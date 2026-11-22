#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
modules/story_codec.py
======================
Standalone lossless codec for Princess Connect! Re:Dive ADV story scripts
and cutscene subtitle Unity AssetBundles (.unity3d).

Binary Story Format Specification:
    - Stream of variable-length records until EOF:
        [uint16 big-endian command_id]
        Repeated argument entries:
            [uint32 big-endian byte_length]
            [byte_length raw bytes]  (terminated when byte_length == 0)
    - Argument Encoding:
        UTF-8 text -> Base64 -> bitwise NOT (~b & 0xFF) on every 3rd byte (index 0, 3, 6, ...).

Lossless v2.1 Text Format:
    - Header: `#!priconne-story v2`
    - One record = command line, one physical line per escaped argument, category line
      (`System`, `Motion`, or `Effect`), and a blank separator line.
    - Unchanged arguments preserve their original raw bytes on repack for byte-exact round-trips.

Dependencies:
    - Binary codec functions (`parse_story`, `build_story_bytes`, `story_to_text`, `text_to_recs`)
      use Python Standard Library ONLY.
    - `.unity3d` container reading/writing requires optional `UnityPy` (`pip install UnityPy`).
"""

from __future__ import annotations

import base64
import binascii
import json
import re
import struct
import warnings
from pathlib import Path
from typing import Any, List, Optional, Tuple

HEADER = "#!priconne-story v2"

COMMANDS: List[str] = [
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

NAME_TO_ID = {name: idx for idx, name in enumerate(COMMANDS)}
CATEGORIES = {"System", "Motion", "Effect"}
MOTION_IDS = set(range(16, 30)) | {60, 66}
EFFECT_IDS = set(range(43, 59))

_ESC_MAP = {
    "\\": "\\\\",
    "\n": "\\n",
    "\r": "\\r",
    "\t": "\\t",
    "\v": "\\v",
    "\f": "\\f",
    "\x85": "\\N",
    "\u2028": "\\L",
    "\u2029": "\\P",
}
_UNESC_MAP = {v[1]: k for k, v in _ESC_MAP.items()}
_UNESC_MAP.update({"s": " ", "S": "\u3000"})
_ESC_RE = re.compile("[" + re.escape("".join(_ESC_MAP)) + "]")


class StoryCodecError(Exception):
    """Raised when a story bundle or script cannot be decoded or verified."""


def command_name(cid: int) -> str:
    return COMMANDS[cid] if cid < len(COMMANDS) else f"unknown_{cid}"


def command_id(name: str) -> int:
    if name in NAME_TO_ID:
        return NAME_TO_ID[name]
    m = re.fullmatch(r"unknown_(\d+)", name) or re.fullmatch(r"(\d+)", name)
    if m:
        return int(m.group(1))
    raise StoryCodecError(f"Unknown ADV command name: {name!r}")


def command_category(cid: int) -> str:
    if cid in MOTION_IDS:
        return "Motion"
    if cid in EFFECT_IDS:
        return "Effect"
    return "System"


def _invert_every_third_byte(payload: bytes) -> bytes:
    """Invert bits on byte indices 0, 3, 6, ... (Priconne ADV obfuscation)."""
    buf = bytearray(payload)
    for i in range(0, len(buf), 3):
        buf[i] = (~buf[i]) & 0xFF
    return bytes(buf)


def decode_arg(raw: bytes) -> str:
    """Decode one obfuscated binary argument into a Python string."""
    inv = _invert_every_third_byte(raw)
    try:
        decoded = base64.b64decode(inv, validate=True)
    except (binascii.Error, ValueError):
        decoded = base64.b64decode(inv)
    return decoded.decode("utf-8", "surrogateescape")


def encode_arg(text: str) -> bytes:
    """Encode a Python string back into Priconne's obfuscated argument format."""
    b64 = base64.b64encode(text.encode("utf-8", "surrogateescape"))
    return _invert_every_third_byte(b64)


def parse_story(data: bytes) -> List[Tuple[int, List[bytes]]]:
    """Parse raw storydata bytes into a list of (command_id, [raw_arg_bytes, ...])."""
    records: List[Tuple[int, List[bytes]]] = []
    pos = 0
    total = len(data)
    while pos < total:
        if pos + 2 > total:
            raise StoryCodecError(f"Trailing bytes at offset {pos}")
        cid = struct.unpack_from(">H", data, pos)[0]
        pos += 2
        args: List[bytes] = []
        while True:
            if pos + 4 > total:
                raise StoryCodecError(f"Truncated argument header at offset {pos}")
            length = struct.unpack_from(">I", data, pos)[0]
            pos += 4
            if length == 0:
                break
            if pos + length > total:
                raise StoryCodecError(f"Truncated argument body at offset {pos}")
            args.append(data[pos : pos + length])
            pos += length
        records.append((cid, args))
    return records


def escape_arg(text: str) -> str:
    """Escape control characters and trailing spaces for lossless 1-line-per-arg output."""
    if any(0xDC80 <= ord(ch) <= 0xDCFF for ch in text):
        raw = text.encode("utf-8", "surrogateescape")
        return "\\b64:" + base64.b64encode(raw).decode("ascii")
    out = _ESC_RE.sub(lambda m: _ESC_MAP[m.group()], text)
    m = re.search(r"[ \u3000]+$", out)
    if m:
        suffix = "".join("\\s" if c == " " else "\\S" for c in m.group())
        out = out[: m.start()] + suffix
    return "\\" + out if out in CATEGORIES else out


def unescape_arg(line: str) -> str:
    """Reverse escape_arg() back into the exact runtime string."""
    if line.startswith("\\b64:"):
        return base64.b64decode(line[5:]).decode("utf-8", "surrogateescape")
    if line.startswith("\\") and line[1:] in CATEGORIES:
        return line[1:]
    out: List[str] = []
    i = 0
    while i < len(line):
        if line[i] == "\\" and i + 1 < len(line) and line[i + 1] in _UNESC_MAP:
            out.append(_UNESC_MAP[line[i + 1]])
            i += 2
        else:
            out.append(line[i])
            i += 1
    return "".join(out)


def story_to_text(decoded_recs: List[Tuple[int, List[str]]]) -> str:
    """Render decoded story records into lossless v2.1 text format."""
    lines = [HEADER]
    for cid, args in decoded_recs:
        lines.append(command_name(cid))
        lines.extend(escape_arg(a) for a in args)
        lines.append(command_category(cid))
        lines.append("")
    return "\r\n".join(lines) + "\r\n"


def text_to_recs(text: str) -> List[Tuple[int, List[str]]]:
    """Parse a v2.1 text file back into (command_id, [decoded_str, ...]) records."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    idx = 1 if lines and lines[0].startswith("#!") else 0
    recs: List[Tuple[int, List[str]]] = []
    while idx < len(lines):
        if lines[idx] == "":
            idx += 1
            continue
        name = lines[idx]
        idx += 1
        cid = command_id(name)
        args: List[str] = []
        while idx < len(lines) and lines[idx] not in CATEGORIES:
            args.append(unescape_arg(lines[idx]))
            idx += 1
        if idx >= len(lines):
            raise StoryCodecError(f"Record #{len(recs)} ({name!r}) missing category terminator")
        idx += 1
        recs.append((cid, args))
    if not recs:
        raise StoryCodecError("No story records found in text file.")
    return recs


def build_story_bytes(
    recs: List[Tuple[int, List[str]]],
    original_recs: Optional[List[Tuple[int, List[bytes]]]] = None,
) -> bytes:
    """
    Serialize records back into Priconne binary format.
    When original_recs is provided, unchanged arguments reuse their exact original bytes.
    """
    out = bytearray()
    orig_list = original_recs or []
    for idx, (cid, args) in enumerate(recs):
        old = orig_list[idx] if idx < len(orig_list) and orig_list[idx][0] == cid else None
        old_decoded = [decode_arg(b) for b in old[1]] if old else []
        out += struct.pack(">H", cid)
        for j, arg in enumerate(args):
            if arg == "":
                continue
            if old is not None and j < len(old_decoded) and old_decoded[j] == arg:
                raw = old[1][j]
            else:
                raw = encode_arg(arg)
            out += struct.pack(">I", len(raw)) + raw
        out += struct.pack(">I", 0)
    return bytes(out)


# ---------------------------------------------------------------------------
# Optional UnityPy Bundle Integration (.unity3d Extract & Repack)
# ---------------------------------------------------------------------------
def _require_unitypy() -> Any:
    try:
        import UnityPy  # type: ignore
        import UnityPy.config  # type: ignore

        UnityPy.config.FALLBACK_UNITY_VERSION = "2021.3.20f1"
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        return UnityPy
    except ImportError as exc:
        raise StoryCodecError(
            "UnityPy is required to read/write .unity3d bundles.\n"
            "Install it with:  pip install UnityPy\n"
            "(Supported on Python 3.10 - 3.14)"
        ) from exc


def _get_script_field(text_asset: Any) -> Tuple[str, Any]:
    for attr in ("m_Script", "script", "text"):
        val = getattr(text_asset, attr, None)
        if val is not None:
            return attr, val
    raise StoryCodecError("TextAsset object has no readable script payload.")


def load_unity_bundle(bundle_path: Path) -> Tuple[Any, str, Any]:
    """Load a .unity3d file and detect whether it holds a 'story' or 'subtitle' asset."""
    UnityPy = _require_unitypy()
    env = UnityPy.load(str(bundle_path))
    story_obj = None
    sub_obj = None

    for obj in env.objects:
        try:
            if obj.type.name == "TextAsset":
                data = obj.read()
                name = getattr(data, "m_Name", "") or ""
                if "story" in name.lower():
                    story_obj = obj
            elif obj.type.name == "MonoBehaviour":
                tree = obj.read_typetree()
                rl = tree.get("recordList")
                if isinstance(rl, list) and rl and isinstance(rl[0], dict) and "text" in rl[0]:
                    sub_obj = obj
        except Exception:
            continue

    if story_obj is not None:
        return env, "story", story_obj
    if sub_obj is not None:
        return env, "subtitle", sub_obj
    raise StoryCodecError(f"No supported story TextAsset or subtitle MonoBehaviour in {bundle_path.name}")


def extract_bundle(bundle_path: Path, out_dir: Path) -> Tuple[str, Path]:
    """
    Extract a .unity3d story or subtitle bundle into `out_dir`.
    Returns (asset_kind, output_file_path).
    """
    _, kind, obj = load_unity_bundle(bundle_path)
    out_dir.mkdir(parents=True, exist_ok=True)

    if kind == "story":
        _, script_val = _get_script_field(obj.read())
        raw = script_val.encode("utf-8", "surrogateescape") if isinstance(script_val, str) else bytes(script_val)
        orig = parse_story(raw)
        decoded = [(cid, [decode_arg(a) for a in args]) for cid, args in orig]
        text = story_to_text(decoded)

        if build_story_bytes(text_to_recs(text), orig) != raw:
            raise StoryCodecError(f"Round-trip verification failed for {bundle_path.name}")

        out_path = out_dir / f"{bundle_path.stem}.txt"
        out_path.write_text(text, encoding="utf-8", newline="")
        return kind, out_path

    rl = obj.read_typetree()["recordList"]
    payload = [
        {
            "id": i + 1,
            "startTime": r["startTime"],
            "endTime": r["endTime"],
            "text": r["text"],
        }
        for i, r in enumerate(rl)
    ]
    out_path = out_dir / f"{bundle_path.stem}.json"
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return kind, out_path


def repack_bundle(bundle_path: Path, translated_path: Path, out_bundle_path: Path) -> str:
    """
    Repack a translated v2 .txt story or .json subtitle file back into a .unity3d bundle.
    Verifies the written story bundle by re-reading it from disk.
    """
    env, kind, obj = load_unity_bundle(bundle_path)
    out_bundle_path.parent.mkdir(parents=True, exist_ok=True)

    if kind == "story":
        attr, current = _get_script_field(obj.read())
        raw_orig = current.encode("utf-8", "surrogateescape") if isinstance(current, str) else bytes(current)
        orig = parse_story(raw_orig)
        new_recs = text_to_recs(translated_path.read_text(encoding="utf-8-sig", newline=""))
        new_bytes = build_story_bytes(new_recs, orig)

        modes = ["str", "bytes"] if isinstance(current, str) else ["bytes", "str"]
        for mode in modes:
            data_obj = obj.read()
            setattr(
                data_obj,
                attr,
                new_bytes.decode("utf-8", "surrogateescape") if mode == "str" else new_bytes,
            )
            data_obj.save()
            out_bundle_path.write_bytes(env.file.save(packer="original"))

            _, kind2, obj2 = load_unity_bundle(out_bundle_path)
            _, back_val = _get_script_field(obj2.read())
            back_bytes = back_val.encode("utf-8", "surrogateescape") if isinstance(back_val, str) else bytes(back_val)
            if kind2 == "story" and back_bytes == new_bytes:
                return f"story repacked ({mode}, verified)"

        out_bundle_path.unlink(missing_ok=True)
        raise StoryCodecError(f"Write verification failed for {bundle_path.name}")

    tree = obj.read_typetree()
    rl = tree["recordList"]
    tl_data = json.loads(translated_path.read_text(encoding="utf-8-sig"))
    if isinstance(tl_data, dict):
        tl_data = tl_data.get("subtitles") or tl_data.get("recordList") or tl_data.get("records")
    if not isinstance(tl_data, list) or len(tl_data) != len(rl):
        raise StoryCodecError("Subtitle JSON entry count does not match original bundle.")
    for orig_item, tl_item in zip(rl, tl_data):
        orig_item["startTime"] = float(tl_item.get("startTime", orig_item["startTime"]))
        orig_item["endTime"] = float(tl_item.get("endTime", orig_item["endTime"]))
        orig_item["text"] = str(tl_item["text"])
    obj.save_typetree(tree)
    out_bundle_path.write_bytes(env.file.save(packer="original"))
    return "subtitle repacked"
