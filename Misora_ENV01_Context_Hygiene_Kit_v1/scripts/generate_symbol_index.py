#!/usr/bin/env python3
"""Read-only AST Symbol Index generator for Misora: Story Editor.

Generates a concise, deterministic Markdown navigation map
(`docs/architecture/MISORA_SYMBOL_INDEX.md`) from `misora.py`, `core/*.py`,
and `assets/*.py` using Python stdlib `ast` only (zero third-party deps,
zero edits to source files).

Usage:
    py -3.12 tools/generate_symbol_index.py
    py -3.12 tools/generate_symbol_index.py --check
"""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

DEFAULT_OUT = Path("docs/architecture/MISORA_SYMBOL_INDEX.md")

DOMAIN_RULES: Sequence[Tuple[str, Sequence[str]]] = (
    ("Splash & Startup", ("splash", "deferred_restore", "_init", "startup", "withdraw", "deiconify")),
    ("File I/O, Save & Workspace", ("open_file", "save", "close_file", "reload", "workspace", "misora", "dirty", "bundle", "backup")),
    ("XUAT Index, Import & Archiving", ("xuat", "archive", "cleanup", "import", "sync")),
    ("MTL & AI Prompt", ("mtl", "translat", "globe", "prompt", "ai_")),
    ("Undo / Redo & Edit Commit", ("undo", "redo", "delta", "commit", "flush", "quick_edit", "box0", "metadata")),
    ("All Script & Virtualized Pool", ("all_script", "continuous", "pool", "card", "virtual")),
    ("Dialogue View, Preview & NGUI", ("dialogue", "preview", "ngui", "ruby", "color", "ruler", "gutter", "wrap", "overflow")),
    ("Selection, Lock, Pin & Speaker", ("select", "lock", "pin", "speaker", "actor", "jump")),
    ("Search & Replace", ("search", "find", "replace")),
    ("Menu, Theme, Icons, Tooltips & Dialogs", ("menu", "theme", "style", "font", "icon", "tooltip", "about", "support", "dialog", "config", "pref")),
)


def classify_domain(symbol_name: str) -> str:
    low = symbol_name.lower()
    for domain, keywords in DOMAIN_RULES:
        if any(kw in low for kw in keywords):
            return domain
    return "Other / Utility"


def collect_target_files(repo_root: Path) -> List[Path]:
    files: List[Path] = []
    for fixed in ("__init__.py", "misora.py"):
        p = repo_root / fixed
        if p.is_file():
            files.append(p)
    for folder in ("core", "assets"):
        d = repo_root / folder
        if d.is_dir():
            files.extend(sorted(p for p in d.glob("*.py") if p.is_file()))
    return files


def parse_file_symbols(path: Path, repo_root: Path) -> Dict[str, object]:
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    line_count = len(text.splitlines())
    tree = ast.parse(text, filename=str(path))

    classes: List[Dict[str, object]] = []
    top_funcs: List[Dict[str, object]] = []

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            end_ln = getattr(node, "end_lineno", node.lineno) or node.lineno
            methods: List[Dict[str, object]] = []
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    m_end = getattr(item, "end_lineno", item.lineno) or item.lineno
                    methods.append(
                        {
                            "name": item.name,
                            "start": item.lineno,
                            "end": m_end,
                            "lines": m_end - item.lineno + 1,
                            "domain": classify_domain(f"{node.name}.{item.name}"),
                        }
                    )
            classes.append(
                {
                    "name": node.name,
                    "start": node.lineno,
                    "end": end_ln,
                    "lines": end_ln - node.lineno + 1,
                    "methods": methods,
                }
            )
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            end_ln = getattr(node, "end_lineno", node.lineno) or node.lineno
            top_funcs.append(
                {
                    "name": node.name,
                    "start": node.lineno,
                    "end": end_ln,
                    "lines": end_ln - node.lineno + 1,
                    "domain": classify_domain(node.name),
                }
            )

    return {
        "rel": path.relative_to(repo_root).as_posix(),
        "bytes": len(raw),
        "lines": line_count,
        "classes": classes,
        "functions": top_funcs,
    }


def render_markdown(repo_root: Path, parsed: Sequence[Dict[str, object]]) -> str:
    out: List[str] = []
    out.append("# Misora: Story Editor — AST Symbol Index")
    out.append("")
    out.append(
        "> **Auto-generated (read-only) by `tools/generate_symbol_index.py`.** "
        "Use this index to locate exact line ranges before reading targeted slices of `misora.py`, `core/*.py`, and `assets/*.py`."
    )
    out.append("")

    # 1. File Size & Line Inventory
    out.append("## 1. Source File Inventory")
    out.append("")
    out.append("| File | Lines | Size (KB) | Classes | Top-Level Functions |")
    out.append("|---|---:|---:|---:|---:|")
    total_lines = 0
    total_bytes = 0
    for info in parsed:
        lines = int(info["lines"])
        nbytes = int(info["bytes"])
        total_lines += lines
        total_bytes += nbytes
        classes = info["classes"]
        funcs = info["functions"]
        out.append(
            f"| `{info['rel']}` | {lines:,} | {nbytes / 1024:.1f} | {len(classes)} | {len(funcs)} |"
        )
    out.append(f"| **TOTAL** | **{total_lines:,}** | **{total_bytes / 1024:.1f}** | — | — |")
    out.append("")

    # 2. Top 20 Largest Methods in misora.py
    misora_info = next((x for x in parsed if x["rel"] == "misora.py"), None)
    if misora_info is not None:
        all_methods: List[Tuple[int, str, int, int, str]] = []
        for cls in misora_info["classes"]:
            for m in cls["methods"]:
                all_methods.append(
                    (int(m["lines"]), f"{cls['name']}.{m['name']}", int(m["start"]), int(m["end"]), str(m["domain"]))
                )
        for fn in misora_info["functions"]:
            all_methods.append(
                (int(fn["lines"]), str(fn["name"]), int(fn["start"]), int(fn["end"]), str(fn["domain"]))
            )
        all_methods.sort(key=lambda t: (-t[0], t[2], t[1]))

        out.append("## 2. Top 20 Largest Methods / Functions in `misora.py`")
        out.append("")
        out.append("| Rank | Symbol | Lines | Span | Domain |")
        out.append("|---:|---|---:|---|---|")
        for rank, (ln_cnt, sym, st, en, dom) in enumerate(all_methods[:20], 1):
            out.append(f"| {rank} | `{sym}` | {ln_cnt} | `L{st}-L{en}` | {dom} |")
        out.append("")

        # 3. Class Overview in misora.py
        out.append("## 3. Classes in `misora.py`")
        out.append("")
        out.append("| Class | Span | Lines | Methods |")
        out.append("|---|---|---:|---:|")
        for cls in misora_info["classes"]:
            out.append(
                f"| `{cls['name']}` | `L{cls['start']}-L{cls['end']}` | {cls['lines']} | {len(cls['methods'])} |"
            )
        out.append("")

        # 4. Domain-Grouped Method Index for misora.py
        out.append("## 4. `misora.py` Domain-Grouped Method Index")
        out.append("")
        by_domain: Dict[str, List[Tuple[str, int, int, int]]] = {}
        for cls in misora_info["classes"]:
            for m in cls["methods"]:
                by_domain.setdefault(str(m["domain"]), []).append(
                    (f"{cls['name']}.{m['name']}", int(m["start"]), int(m["end"]), int(m["lines"]))
                )
        for fn in misora_info["functions"]:
            by_domain.setdefault(str(fn["domain"]), []).append(
                (str(fn["name"]), int(fn["start"]), int(fn["end"]), int(fn["lines"]))
            )

        domain_order = [d for d, _ in DOMAIN_RULES] + ["Other / Utility"]
        for dom in domain_order:
            items = by_domain.get(dom)
            if not items:
                continue
            items.sort(key=lambda x: (x[1], x[0]))
            out.append(f"### {dom} ({len(items)})")
            out.append("")
            out.append("| Symbol | Span | Lines |")
            out.append("|---|---|---:|")
            for sym, st, en, ln_cnt in items:
                out.append(f"| `{sym}` | `L{st}-L{en}` | {ln_cnt} |")
            out.append("")

    # 5. Core & Assets Module Index
    out.append("## 5. `core/*.py` & `assets/*.py` Symbol Summary")
    out.append("")
    for info in parsed:
        rel = str(info["rel"])
        if rel in ("__init__.py", "misora.py"):
            continue
        out.append(f"### `{rel}` ({info['lines']} lines, {int(info['bytes']) / 1024:.1f} KB)")
        out.append("")
        rows: List[Tuple[str, str, int]] = []
        for cls in info["classes"]:
            rows.append((f"class `{cls['name']}`", f"`L{cls['start']}-L{cls['end']}`", int(cls["lines"])))
            for m in cls["methods"]:
                rows.append((f"`{cls['name']}.{m['name']}`", f"`L{m['start']}-L{m['end']}`", int(m["lines"])))
        for fn in info["functions"]:
            rows.append((f"`{fn['name']}`", f"`L{fn['start']}-L{fn['end']}`", int(fn["lines"])))
        if rows:
            out.append("| Symbol | Span | Lines |")
            out.append("|---|---|---:|")
            for sym, span, ln_cnt in rows:
                out.append(f"| {sym} | {span} | {ln_cnt} |")
            out.append("")
        else:
            out.append("*(No top-level classes or functions)*")
            out.append("")

    return "\n".join(out).rstrip() + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Misora AST Symbol Index (read-only on source).")
    parser.add_argument("--root", type=Path, default=Path("."), help="Repository root directory")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Output Markdown path relative to root")
    parser.add_argument("--check", action="store_true", help="Exit non-zero if output file differs from generated content")
    args = parser.parse_args(argv)

    repo_root = args.root.resolve()
    out_path = args.out if args.out.is_absolute() else (repo_root / args.out)

    files = collect_target_files(repo_root)
    parsed = [parse_file_symbols(p, repo_root) for p in files]
    rendered = render_markdown(repo_root, parsed)

    if args.check:
        if not out_path.is_file():
            print(f"[CHECK FAILED] Missing index file: {out_path}", file=sys.stderr)
            return 1
        existing = out_path.read_text(encoding="utf-8")
        if existing != rendered:
            print(f"[CHECK FAILED] Index out of date: {out_path}", file=sys.stderr)
            return 1
        print(f"[CHECK OK] {out_path.relative_to(repo_root).as_posix()} is up to date ({len(rendered.encode('utf-8'))} bytes).")
        return 0

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"[WROTE] {out_path.relative_to(repo_root).as_posix()} ({len(rendered.encode('utf-8'))} bytes, {len(files)} source files indexed).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
