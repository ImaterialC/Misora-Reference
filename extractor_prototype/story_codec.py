#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extractor_prototype.story_codec
================================
Pillar 2: High-performance in-memory streaming codec for Priconne ADV story bundles.
Transforms binary story bytes into Cutscene Script Interchange Format (CSIF)
without writing intermediate flat JSON files to disk.
"""

from __future__ import annotations

import base64
import binascii
import io
import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Optional, Tuple, Union


COMMAND_NAMES = [
    "title", "outline", "chara", "visible", "type", "face", "focus", "background",
    "print", "tag", "goto", "bgm", "touch", "choice", "vo", "wait",
    "in_L", "in_R", "out_L", "out_R", "fadein", "fadeout", "in_float", "out_float",
    "jump", "shake", "pop", "nod", "question_right", "question_left", "se", "black_out",
    "black_in", "white_out", "white_in", "transition", "situation", "color_fadein", "flash", "shake_text",
    "text_size", "shake_screen", "double", "flower_y", "flower_r", "concent", "find_l", "find_r",
    "laugh_l", "laugh_r", "chord_l", "chord_r", "sweat_l", "sweat_r", "question_l", "question_r",
    "angry", "drop_l", "drop_r", "live", "scale", "title_telop", "window_visible", "log",
    "novoice", "attract", "change", "fadeout_all",
]

NAME_TO_CID = {name: idx for idx, name in enumerate(COMMAND_NAMES)}


@dataclass
class DialogueBlock:
    """Represents a spoken dialogue line or narrative caption in a scene."""
    speaker: str
    text: str
    voice_clip: Optional[str] = None
    character_id: Optional[int] = None
    cmd_name: str = "print"


@dataclass
class StoryScene:
    """Represents a fully decoded ADV cutscene."""
    title: str = ""
    outline: str = ""
    dialogues: List[DialogueBlock] = field(default_factory=list)
    commands: List[Tuple[str, List[str]]] = field(default_factory=list)

    def to_csif(self) -> str:
        """
        Export scene directly into Cutscene Script Interchange Format (CSIF).
        CSIF uses @@Speaker headers followed by dialogue text blocks.
        """
        lines: List[str] = ["# CSIF Cutscene Script Interchange Format"]
        if self.title:
            lines.append(f"# Title: {self.title}")
        if self.outline:
            lines.append(f"# Outline: {self.outline}")
        lines.append("")

        for d in self.dialogues:
            header = f"@@{d.speaker}" if d.speaker else "@@"
            if d.voice_clip:
                header += f" [voice={d.voice_clip}]"
            lines.append(header)
            lines.append(d.text)
            lines.append("")

        return "\n".join(lines).strip() + "\n"


class StoryCodec:
    """High-speed in-memory parser and codec for Priconne ADV bytecode."""

    @staticmethod
    def invert_every_third_byte(payload: bytes) -> bytes:
        """Bitwise NOT on every third byte (offsets 0, 3, 6, ...) of payload."""
        buf = bytearray(payload)
        for i in range(0, len(buf), 3):
            buf[i] = (~buf[i]) & 0xFF
        return bytes(buf)

    @classmethod
    def decode_arg(cls, raw: bytes) -> str:
        """Decode one obfuscated ADV argument byte sequence into UTF-8 text."""
        inv = cls.invert_every_third_byte(raw)
        try:
            decoded = base64.b64decode(inv, validate=True)
        except (binascii.Error, ValueError):
            decoded = base64.b64decode(inv)
        return decoded.decode("utf-8", "surrogateescape")

    @classmethod
    def encode_arg(cls, text: str) -> bytes:
        """Encode UTF-8 text into Priconne's obfuscated binary argument format."""
        b64 = base64.b64encode(text.encode("utf-8", "surrogateescape"))
        return cls.invert_every_third_byte(b64)

    @classmethod
    def parse_raw_bytecode(cls, data: bytes) -> List[Tuple[int, List[bytes]]]:
        """
        Parse raw story binary payload into (cmd_id, [raw_arg_bytes, ...]).
        Stream structure:
            uint16 cmd_id
            repeated:
                uint32 length
                length bytes (terminated by length == 0)
        """
        records: List[Tuple[int, List[bytes]]] = []
        pos = 0
        total = len(data)
        while pos < total:
            if pos + 2 > total:
                break
            cid = struct.unpack_from(">H", data, pos)[0]
            pos += 2
            args: List[bytes] = []
            while True:
                if pos + 4 > total:
                    break
                length = struct.unpack_from(">I", data, pos)[0]
                pos += 4
                if length == 0:
                    break
                if pos + length > total:
                    break
                args.append(data[pos : pos + length])
                pos += length
            records.append((cid, args))
        return records

    @classmethod
    def build_raw_bytecode(cls, records: List[Tuple[int, List[bytes]]]) -> bytes:
        """Serialize (cmd_id, [raw_arg_bytes, ...]) back into binary story payload."""
        out = bytearray()
        for cid, args in records:
            out.extend(struct.pack(">H", cid))
            for a in args:
                out.extend(struct.pack(">I", len(a)))
                out.extend(a)
            out.extend(struct.pack(">I", 0))
        return bytes(out)

    @classmethod
    def decode_scene_from_bytes(cls, data: bytes) -> StoryScene:
        """Parse raw binary story data directly into a high-level StoryScene."""
        raw_records = cls.parse_raw_bytecode(data)
        scene = StoryScene()
        current_voice = ""
        current_speaker = ""

        for cid, raw_args in raw_records:
            cmd_name = COMMAND_NAMES[cid] if cid < len(COMMAND_NAMES) else f"cmd_{cid}"
            decoded_args = [cls.decode_arg(a) for a in raw_args]
            scene.commands.append((cmd_name, decoded_args))

            if cmd_name == "title" and decoded_args:
                scene.title = decoded_args[0]
            elif cmd_name == "outline" and decoded_args:
                scene.outline = decoded_args[0]
            elif cmd_name == "vo" and decoded_args:
                current_voice = decoded_args[0]
            elif cmd_name == "touch" and decoded_args and decoded_args[0].startswith("vo_"):
                current_voice = decoded_args[0]
            elif cmd_name == "tag" and len(decoded_args) >= 1:
                # tag defines speaker or narrator tag
                current_speaker = decoded_args[0]
            elif cmd_name == "print":
                if len(decoded_args) >= 2:
                    speaker = decoded_args[0]
                    text = decoded_args[1]
                elif len(decoded_args) == 1:
                    speaker = current_speaker
                    text = decoded_args[0]
                else:
                    continue

                scene.dialogues.append(
                    DialogueBlock(
                        speaker=speaker,
                        text=text,
                        voice_clip=current_voice if current_voice else None,
                        cmd_name="print",
                    )
                )
                current_voice = ""

        return scene

    @classmethod
    def decode_from_bundle(cls, bundle_source: Union[Path, bytes, io.BytesIO]) -> StoryScene:
        """
        Load a Unity AssetBundle (.unity3d) in-memory using UnityPy and extract StoryScene.
        """
        try:
            import UnityPy  # type: ignore
        except ImportError as exc:
            raise RuntimeError("UnityPy is required to unpack .unity3d bundles. Install with: pip install UnityPy") from exc

        if isinstance(bundle_source, (bytes, bytearray)):
            env = UnityPy.load(io.BytesIO(bundle_source))
        elif isinstance(bundle_source, io.BytesIO):
            env = UnityPy.load(bundle_source)
        else:
            env = UnityPy.load(str(bundle_source))

        for obj in env.objects:
            if obj.type.name == "TextAsset":
                data = obj.read()
                name = getattr(data, "m_Name", "") or ""
                if "story" in name.lower():
                    for attr in ("m_Script", "script", "text"):
                        val = getattr(data, attr, None)
                        if val is not None:
                            raw = val.encode("utf-8", "surrogateescape") if isinstance(val, str) else bytes(val)
                            return cls.decode_scene_from_bytes(raw)

        raise ValueError("No valid story TextAsset found inside asset bundle.")
