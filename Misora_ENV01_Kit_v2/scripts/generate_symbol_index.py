#!/usr/bin/env python3
"""Generate a deterministic, read-only AST navigation index for Misora.

Reads Python source only and writes only the Markdown output. It never imports
Misora modules or modifies source files. The index is a navigation aid, not
proof of runtime reachability, test coverage, or dead code.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import subprocess
import sys
from pathlib import Path
from typing import Iterable

DEFAULT_OUTPUT = Path("docs/architecture/MISORA_SYMBOL_INDEX.md")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


INDEXED_PATHSPECS = ("__init__.py", "misora.py", ":(glob)core/*.py", ":(glob)assets/*.py")


def indexed_source_revision(root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H", "HEAD", "--", *INDEXED_PATHSPECS],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
        )
    except (OSError, subprocess.CalledProcessError, UnicodeError) as exc:
        raise RuntimeError(f"Unable to read Indexed Source Revision: {exc}") from exc
    rev = result.stdout.strip()
    if len(rev) < 40 or any(ch not in "0123456789abcdefABCDEF" for ch in rev):
        raise RuntimeError(f"Unexpected Indexed Source Revision value: {rev!r}")
    return rev.lower()


def check_clean_indexed_sources(root: Path) -> None:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain=v1", "--ignored=matching", "--untracked-files=all", "--", *INDEXED_PATHSPECS],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
        )
    except (OSError, subprocess.CalledProcessError, UnicodeError) as exc:
        raise RuntimeError(f"Unable to verify clean indexed sources: {exc}") from exc
    dirty = [line for line in result.stdout.splitlines() if line.strip()]
    if dirty:
        raise RuntimeError(
            "Indexed Python source files have uncommitted, untracked, or ignored changes:\n"
            + "\n".join(dirty)
        )


def indexed_paths(root: Path) -> list[Path]:
    candidates: list[Path] = [root / "__init__.py", root / "misora.py"]
    for folder in (root / "core", root / "assets"):
        if folder.exists():
            candidates.extend(folder.glob("*.py"))
    missing = [p for p in (root / "__init__.py", root / "misora.py") if not p.is_file()]
    if missing:
        names = ", ".join(p.relative_to(root).as_posix() for p in missing)
        raise RuntimeError(f"Required source file(s) missing: {names}")
    paths = {p.resolve() for p in candidates if p.is_file()}
    try:
        return sorted(paths, key=lambda p: p.relative_to(root).as_posix())
    except ValueError as exc:
        raise RuntimeError("An indexed source path resolves outside the repository root") from exc


def signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    try:
        return ast.unparse(node.args)
    except Exception:
        return "signature unavailable"


def domain_for(path: str, name: str) -> str:
    """Heuristic grouping only; not a semantic classification."""
    probe = f"{path} {name}".lower()
    rules = (
        ("AST / serialization", ("story_ast", "record", "box", "binary", "codec", "serialize", "parse")),
        ("Bundle / persistence", ("bundle", "save", "load", "backup", "atomic", "workspace")),
        ("XUAT / text IO", ("xuat", "dictionary", "encoding", "text_file")),
        ("Search", ("search", "matcher", "replace")),
        ("UI / Tk", ("misora.py", "dialog", "widget", "view", "ribbon", "tooltip", "splash", "icon")),
        ("Undo / document lifecycle", ("undo", "redo", "delta", "document", "journal")),
        ("MTL / network", ("mtl", "translate", "deepl", "http", "security")),
        ("NGUI / CSIF", ("ngui", "tag", "csif", "script_codec")),
    )
    for label, needles in rules:
        if any(token in probe for token in needles):
            return label
    return "Other / unclassified"


def parse_file(path: Path, root: Path) -> tuple[str, str, list[dict[str, object]]]:
    raw = path.read_bytes()
    # Strict decoding is intentional: malformed input must fail loudly.
    source = raw.decode("utf-8", errors="strict")
    rel = path.relative_to(root).as_posix()
    tree = ast.parse(source, filename=rel)
    rows: list[dict[str, object]] = []

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            rows.append({
                "kind": "async function" if isinstance(node, ast.AsyncFunctionDef) else "function",
                "name": node.name,
                "line": node.lineno,
                "signature": signature(node),
                "domain": domain_for(rel, node.name),
            })
        elif isinstance(node, ast.ClassDef):
            rows.append({
                "kind": "class",
                "name": node.name,
                "line": node.lineno,
                "signature": "",
                "domain": domain_for(rel, node.name),
            })
            # Index immediate class methods only; nested declarations are out of scope.
            for member in node.body:
                if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    rows.append({
                        "kind": "async method" if isinstance(member, ast.AsyncFunctionDef) else "method",
                        "name": f"{node.name}.{member.name}",
                        "line": member.lineno,
                        "signature": signature(member),
                        "domain": domain_for(rel, f"{node.name}.{member.name}"),
                    })

    rows.sort(key=lambda row: (int(row["line"]), str(row["kind"]), str(row["name"])))
    return rel, sha256(raw), rows


def render(root: Path) -> str:
    check_clean_indexed_sources(root)
    rev = indexed_source_revision(root)
    parsed = [parse_file(path, root) for path in indexed_paths(root)]
    lines = [
        "# Misora — AST Symbol Index",
        "",
        "> Generated by `tools/generate_symbol_index.py`. Deterministic output; no timestamp.",
        "> **Navigation aid only:** declarations do not prove runtime reachability, call relationships, test coverage, safety, or dead code.",
        "> Domain grouping is heuristic, not semantic classification.",
        "",
        f"- Indexed Source Revision: `{rev}`",
        f"- Indexed Python files: {len(parsed)}",
        "- Parser: Python `ast` (stdlib); UTF-8 decoding is strict.",
        "",
        "## Source fingerprints",
        "",
        "| File | SHA-256 | AST declarations |",
        "|---|---|---:|",
    ]
    for rel, digest, rows in parsed:
        lines.append(f"| `{rel}` | `{digest}` | {len(rows)} |")

    lines.extend(["", "## Symbols", ""])
    all_rows = [(rel, row) for rel, _digest, rows in parsed for row in rows]
    if not all_rows:
        lines.append("No top-level functions/classes or immediate class methods were found.")
    else:
        lines.extend([
            "| Domain (heuristic) | File | Line | Kind | Symbol | Signature |",
            "|---|---|---:|---|---|---|",
        ])
        for rel, row in all_rows:
            name = str(row["name"]).replace("|", "\\|")
            sig = str(row["signature"]).replace("|", "\\|").replace("`", "\\`")
            lines.append(f"| {row['domain']} | `{rel}` | {row['line']} | {row['kind']} | `{name}` | `{sig}` |")
    lines.extend([
        "",
        "## Safe use",
        "",
        "1. Check the embedded Indexed Source Revision and per-file fingerprints against the current working tree.",
        "2. Open actual source around the indexed line and inspect relevant helpers/callers as needed.",
        "3. Inspect narrow tests and reproduce runtime behavior for bug reports.",
        "4. Do not infer dead code from absence here: dynamic dispatch, callbacks, Tk bindings, plugin hooks, and reflection may not appear as direct AST references.",
        "",
    ])
    return "\n".join(lines)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="Misora repository root")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output Markdown path, relative to root unless absolute")
    parser.add_argument("--check", action="store_true", help="Compare generated output without writing")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    allowed_output = (root / DEFAULT_OUTPUT).resolve()
    output = (args.output if args.output.is_absolute() else root / args.output).resolve()
    if output != allowed_output:
        print(
            f"ERROR: output path must resolve to {allowed_output} (got {output})",
            file=sys.stderr,
        )
        return 2
    try:
        expected = render(root)
        display_path = output.relative_to(root).as_posix() if output.is_relative_to(root) else str(output)
        if args.check:
            if not output.is_file():
                print(f"CHECK FAIL: output does not exist: {display_path}", file=sys.stderr)
                return 1
            current = output.read_bytes()
            if current != expected.encode("utf-8"):
                print(f"CHECK FAIL: generated index differs: {display_path}", file=sys.stderr)
                return 1
            print(f"CHECK PASS: {display_path}")
            return 0
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(expected, encoding="utf-8", newline="\n")
        print(f"WROTE: {display_path}")
        return 0
    except (OSError, UnicodeError, SyntaxError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
