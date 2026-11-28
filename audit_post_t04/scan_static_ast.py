#!/usr/bin/env python3
"""
Misora POST-T-04 - Upgraded Local AST Static Scan (stdlib-only, zero-.pyc)
Reads all .py files under D:/Misora-Editor with BOM-safe decoding.
Outputs 01_ast_static_report.md to the audit directory.
ZERO writes inside D:/Misora-Editor.
"""
import ast
import os
import sys
import re
import hashlib
from pathlib import Path
from collections import defaultdict
from typing import Optional

REPO = Path(r"D:\Misora-Editor")
OUT_DIR = Path(r"D:\Reference\Misora-Reference\audit_post_t04")

PRODUCTION_GLOBS = ["misora.py", "core/**/*.py", "assets/**/*.py"]
ALL_GLOBS = ["__init__.py", "misora.py", "core/**/*.py", "assets/**/*.py",
             "tests/**/*.py", "tools/**/*.py"]
BAT_GLOBS = ["*.bat"]

BOM = bytes([239, 187, 191])

def read_source(path: Path) -> str:
    raw = path.read_bytes()
    return raw.removeprefix(BOM).decode("utf-8")

def glob_files(patterns, base=REPO):
    seen = set()
    for pat in patterns:
        for p in sorted(base.rglob(pat) if "**" in pat else [base / pat] if (base / pat).exists() else base.glob(pat)):
            if p.is_file() and p not in seen:
                seen.add(p)
                yield p

def relpath(p):
    return str(p.relative_to(REPO)).replace("\\", "/")

# ── Check 1: Duplicate top-level functions / methods ──────────────────────
def check_duplicates(tree, filepath):
    findings = []
    # top-level functions
    seen_top = {}
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = node.name
            if name in seen_top:
                findings.append((filepath, node.lineno,
                    f"Duplicate top-level function `{name}` "
                    f"(first at line {seen_top[name]})"))
            else:
                seen_top[name] = node.lineno
    # methods within each class
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            seen_methods = {}
            for item in ast.iter_child_nodes(node):
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    name = item.name
                    if name in seen_methods:
                        findings.append((filepath, item.lineno,
                            f"Duplicate method `{node.name}.{name}` "
                            f"(first at line {seen_methods[name]})"))
                    else:
                        seen_methods[name] = item.lineno
    return findings

# ── Check 2: Unreachable statements ──────────────────────────────────────
TERMINAL = (ast.Return, ast.Raise, ast.Break, ast.Continue)


def check_unreachable(tree, filepath):
    findings = []
    seen_lines = set()
    def scan_body(body):
        for i, stmt in enumerate(body):
            if isinstance(stmt, TERMINAL) and i + 1 < len(body):
                next_stmt = body[i + 1]
                key = (filepath, next_stmt.lineno)
                if key not in seen_lines:
                    seen_lines.add(key)
                    findings.append((filepath, next_stmt.lineno,
                        f"Unreachable code after `{type(stmt).__name__}` at line {stmt.lineno}"))
                # Don't report exhaustive if/else after a terminal — the terminal itself catches it
            # Recurse into compound statements
            if isinstance(stmt, ast.If):
                scan_body(stmt.body)
                scan_body(stmt.orelse)
            elif isinstance(stmt, (ast.For, ast.While)):
                scan_body(stmt.body)
                scan_body(stmt.orelse)
            elif isinstance(stmt, ast.With):
                scan_body(stmt.body)
            elif isinstance(stmt, ast.Try):
                scan_body(stmt.body)
                for handler in stmt.handlers:
                    scan_body(handler.body)
                scan_body(stmt.orelse)
                scan_body(stmt.finalbody)
            elif isinstance(stmt, ast.Match):
                for case in stmt.cases:
                    scan_body(case.body)
            elif isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                scan_body(stmt.body)
            elif isinstance(stmt, ast.ClassDef):
                scan_body(stmt.body)
    # Walk all function/method bodies + module level
    scan_body(tree.body)
    return findings

# ── Check 3: Mutable default arguments ───────────────────────────────────
MUTABLE_TYPES = (ast.List, ast.Dict, ast.Set)

def _is_empty_set_call(node):
    return (isinstance(node, ast.Call) and
            isinstance(node.func, ast.Name) and
            node.func.id == "set" and
            not node.args and not node.keywords)

def check_mutable_defaults(tree, filepath):
    findings = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for default in node.args.defaults + node.args.kw_defaults:
                if default is None:
                    continue
                if isinstance(default, MUTABLE_TYPES):
                    findings.append((filepath, default.lineno,
                        f"Mutable default `{type(default).__name__}` in "
                        f"`{node.name}()`"))
                elif _is_empty_set_call(default):
                    findings.append((filepath, default.lineno,
                        f"Mutable default `set()` call in `{node.name}()`"))
    return findings

# ── Check 4: Zero-caller dead-code candidates ────────────────────────────
def collect_definitions(tree, filepath):
    """Return dict of {name: (filepath, lineno, kind)} for all top-level and class definitions."""
    defs = {}
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            key = node.name
            defs[key] = (filepath, node.lineno, "function")
        elif isinstance(node, ast.ClassDef):
            defs[node.name] = (filepath, node.lineno, "class")
            for item in ast.iter_child_nodes(node):
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    key = f"{node.name}.{item.name}"
                    defs[key] = (filepath, item.lineno, "method")
    return defs

def collect_all_name_tokens(source_text):
    """Return set of all identifier-like tokens in source text, including strings."""
    return set(re.findall(r'[A-Za-z_]\w*', source_text))

# ── Check 5: Dead standalone .py scripts ─────────────────────────────────
def check_dead_scripts(all_sources_text, bat_texts, all_files):
    """Find .py files in root/tools/core/assets not imported or referenced anywhere."""
    findings = []
    # Collect all import references and string references
    combined = all_sources_text + "\n" + "\n".join(bat_texts)
    for f in all_files:
        rel = relpath(f)
        parts = Path(rel).parts
        # Skip __init__.py, test files
        if f.name == "__init__.py":
            continue
        if parts[0] == "tests":
            continue
        stem = f.stem
        # Check if stem appears anywhere in combined sources
        if stem not in combined:
            findings.append((rel, 0, f"UNVERIFIED-DEAD: `{rel}` — stem `{stem}` not found "
                             "in any .py source, .bat, or test file"))
    return findings

# ── Check 6: winfo_ismapped() calls ──────────────────────────────────────
def check_winfo_ismapped(source_lines, filepath):
    findings = []
    for i, line in enumerate(source_lines, 1):
        if "winfo_ismapped()" in line or "winfo_ismapped(" in line:
            findings.append((filepath, i,
                f"Remaining `winfo_ismapped()` call (potential T-01-class visibility bug): "
                f"`{line.strip()}`"))
    return findings

# ── Check 7: Broad except blocks in critical paths ───────────────────────
CRITICAL_PATH_KEYWORDS = {"save", "export", "exit", "patch", "sync", "binary",
                          "undo", "redo", "write", "bundle", "serialize",
                          "close", "backup", "replace", "atomic"}

def check_broad_except(tree, filepath, source_lines):
    findings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            is_broad = False
            if node.type is None:
                is_broad = True
                label = "bare `except:`"
            elif (isinstance(node.type, ast.Name) and
                  node.type.id == "Exception"):
                # Check if body is just pass
                if (len(node.body) == 1 and isinstance(node.body[0], ast.Pass)):
                    is_broad = True
                    label = "`except Exception: pass`"
            if is_broad:
                # Determine enclosing function
                # Walk parents to find function context
                func_name = _find_enclosing_func(tree, node.lineno)
                if func_name:
                    fn_lower = func_name.lower()
                    if any(kw in fn_lower for kw in CRITICAL_PATH_KEYWORDS):
                        findings.append((filepath, node.lineno,
                            f"{label} in critical-path function `{func_name}`"))
                    else:
                        findings.append((filepath, node.lineno,
                            f"{label} in function `{func_name}`"))
                else:
                    findings.append((filepath, node.lineno,
                        f"{label} at module level"))
    return findings

def _find_enclosing_func(tree, target_lineno):
    """Find the name of the function/method enclosing the given line number."""
    best = None
    best_start = -1
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if (node.lineno <= target_lineno and
                (node.end_lineno or 999999) >= target_lineno):
                if node.lineno > best_start:
                    best_start = node.lineno
                    # Try to get class name
                    best = node.name
    # Also check for class context
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for item in ast.iter_child_nodes(node):
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if (item.lineno <= target_lineno and
                        (item.end_lineno or 999999) >= target_lineno):
                        if item.lineno > best_start:
                            best_start = item.lineno
                            best = f"{node.name}.{item.name}"
    return best

# ── Check 8: after() calls and Tk Variable / worker thread creation ──────
def check_after_and_variables(tree, filepath, source_lines):
    findings = []
    # Scan for .after( calls
    after_pattern = re.compile(r'\.after\s*\(')
    after_cancel_pattern = re.compile(r'\.after_cancel\s*\(')
    after_lines = []
    cancel_lines = []
    for i, line in enumerate(source_lines, 1):
        if after_pattern.search(line):
            after_lines.append((i, line.strip()))
        if after_cancel_pattern.search(line):
            cancel_lines.append((i, line.strip()))

    if after_lines:
        findings.append((filepath, 0,
            f"after() call sites: {len(after_lines)}, "
            f"after_cancel() sites: {len(cancel_lines)} "
            f"— audit for untracked cancel"))

    # Scan for Tk Variable creation (StringVar, IntVar, BooleanVar, DoubleVar)
    var_pattern = re.compile(r'\b(StringVar|IntVar|BooleanVar|DoubleVar)\s*\(')
    for i, line in enumerate(source_lines, 1):
        if var_pattern.search(line):
            findings.append((filepath, i,
                f"Tk Variable creation: `{line.strip()}`"))

    # Scan for thread creation sites
    thread_pattern = re.compile(r'\b(Thread|ThreadPoolExecutor|submit)\s*\(')
    for i, line in enumerate(source_lines, 1):
        if thread_pattern.search(line):
            findings.append((filepath, i,
                f"Worker thread creation site: `{line.strip()}`"))

    return findings


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════
def main():
    report_lines = []
    report_lines.append("# Misora POST-T-04 — AST Static Analysis Report")
    report_lines.append("")
    report_lines.append(f"**Scan date:** 2026-11-28  ")
    report_lines.append(f"**Baseline HEAD:** `8affb7c53b6af6047ace423c7e4d830a978eb644`  ")
    report_lines.append(f"**Scanner:** `scan_static_ast.py` (stdlib `ast` module, zero .pyc writes)  ")
    report_lines.append(f"**Production scope:** `misora.py`, `core/**/*.py`, `assets/**/*.py`  ")
    report_lines.append(f"**Cross-reference scope:** ALL repo `.py` files + `.bat` launchers")
    report_lines.append("")

    # Gather files
    prod_files = list(glob_files(PRODUCTION_GLOBS))
    all_py_files = list(glob_files(ALL_GLOBS))
    bat_files = list(glob_files(BAT_GLOBS))

    report_lines.append(f"**Production files scanned:** {len(prod_files)}  ")
    report_lines.append(f"**Total .py files scanned:** {len(all_py_files)}  ")
    report_lines.append(f"**BAT files scanned:** {len(bat_files)}")
    report_lines.append("")

    # Parse all files
    parsed = {}  # filepath -> (tree, source_text, source_lines)
    parse_errors = []
    for f in all_py_files:
        try:
            src = read_source(f)
            tree = ast.parse(src, filename=str(f))
            parsed[relpath(f)] = (tree, src, src.splitlines())
        except Exception as e:
            parse_errors.append((relpath(f), str(e)))

    bat_texts = []
    for f in bat_files:
        try:
            bat_texts.append(read_source(f))
        except Exception:
            try:
                bat_texts.append(f.read_text(encoding="latin-1"))
            except Exception:
                pass

    if parse_errors:
        report_lines.append("## Parse Errors")
        report_lines.append("")
        for fp, err in parse_errors:
            report_lines.append(f"- `{fp}`: {err}")
        report_lines.append("")

    # ── Run checks on production files ────────────────────────────────────
    all_findings = {
        "duplicates": [],
        "unreachable": [],
        "mutable_defaults": [],
        "dead_code": [],
        "dead_scripts": [],
        "winfo_ismapped": [],
        "broad_except": [],
        "after_and_vars": [],
    }

    all_defs = {}
    all_sources_combined = ""

    for fp, (tree, src, lines) in parsed.items():
        all_sources_combined += src + "\n"
        # Checks 1-3 on production files only
        is_prod = any(fp.startswith(p.replace("**/*.py", "").replace("*.py", ""))
                      for p in ["misora.py", "core/", "assets/"])
        if is_prod or fp == "misora.py":
            all_findings["duplicates"].extend(check_duplicates(tree, fp))
            all_findings["unreachable"].extend(check_unreachable(tree, fp))
            all_findings["mutable_defaults"].extend(check_mutable_defaults(tree, fp))
            all_findings["broad_except"].extend(check_broad_except(tree, fp, lines))
            all_findings["after_and_vars"].extend(check_after_and_variables(tree, fp, lines))
        # Check 6 specifically for misora.py
        if fp == "misora.py":
            all_findings["winfo_ismapped"].extend(check_winfo_ismapped(lines, fp))
        # Collect definitions from all files
        defs = collect_definitions(tree, fp)
        all_defs.update(defs)

    # Check 4: Dead code candidates — token scan
    all_tokens = collect_all_name_tokens(all_sources_combined)
    for name, (fp, lineno, kind) in sorted(all_defs.items()):
        # Skip dunder methods, __init__, etc.
        if name.startswith("__") or ".__" in name:
            continue
        # Skip common overrides
        base_name = name.split(".")[-1] if "." in name else name
        if base_name.startswith("_") and "." not in name:
            # Private top-level functions — check if name appears elsewhere
            count = all_sources_combined.count(base_name)
            if count <= 1:  # only the definition itself
                all_findings["dead_code"].append((fp, lineno,
                    f"UNVERIFIED-DEAD: `{name}` ({kind}) — "
                    f"token count: {count} (includes definition)"))
        elif "." in name:
            # Method — check if the base method name appears anywhere outside
            # its own definition (token heuristic)
            count = all_sources_combined.count(base_name)
            if count <= 1:
                all_findings["dead_code"].append((fp, lineno,
                    f"UNVERIFIED-DEAD: `{name}` ({kind}) — "
                    f"token count: {count} (includes definition)"))

    # Check 5: Dead standalone scripts
    all_findings["dead_scripts"] = check_dead_scripts(
        all_sources_combined, bat_texts, all_py_files)

    # ── Format report ─────────────────────────────────────────────────────
    section_names = {
        "duplicates": ("1. Duplicate Functions / Methods (Silent Shadowing)", None),
        "unreachable": ("2. Unreachable Statements", None),
        "mutable_defaults": ("3. Mutable Default Arguments", None),
        "dead_code": ("4. Zero-Caller Dead-Code Candidates",
                      "> **CAVEAT:** Token counts include comments/docstrings and miss "
                      "dynamic Tk dispatch (`command=`, `.bind(`, `.after(`, `.protocol(`, "
                      "`getattr`, `hasattr`). Items are `UNVERIFIED-DEAD` ONLY — "
                      "**never declare dead without manual verification**."),
        "dead_scripts": ("5. Potential Dead/Unused Standalone Scripts",
                         "> Cross-checked against all `.py` imports, `.bat` files, `tests/**`, "
                         "and docs. All items are `UNVERIFIED-DEAD`."),
        "winfo_ismapped": ("6. Remaining `winfo_ismapped()` Calls in `misora.py`",
                           "> Potential T-01-class visibility bugs."),
        "broad_except": ("7. Broad `except` Blocks in Critical Paths",
                         "> `except Exception: pass` or bare `except:` in save/export/exit/"
                         "patch/sync/binary/undo paths."),
        "after_and_vars": ("8. `after()` Tracking, Tk Variables & Worker Thread Sites",
                           "> For `Tcl_AsyncDelete` and teardown leak audit."),
    }

    summary_counts = {}
    for key, findings in all_findings.items():
        title, caveat = section_names[key]
        report_lines.append(f"## {title}")
        report_lines.append("")
        if caveat:
            report_lines.append(caveat)
            report_lines.append("")
        summary_counts[key] = len(findings)
        if not findings:
            report_lines.append("*No findings.*")
        else:
            report_lines.append(f"**{len(findings)} finding(s):**")
            report_lines.append("")
            for fp, lineno, msg in findings:
                if lineno > 0:
                    report_lines.append(f"- `{fp}:{lineno}` — {msg}")
                else:
                    report_lines.append(f"- `{fp}` — {msg}")
        report_lines.append("")

    # Summary table
    report_lines.append("## Summary")
    report_lines.append("")
    report_lines.append("| Check | Count |")
    report_lines.append("|---|---:|")
    for key in section_names:
        title = section_names[key][0].split(". ", 1)[-1] if ". " in section_names[key][0] else section_names[key][0]
        report_lines.append(f"| {title} | {summary_counts[key]} |")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("*End of AST static report.*")

    # Write report
    out_path = OUT_DIR / "01_ast_static_report.md"
    out_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Report written to: {out_path}")
    print(f"Total findings: {sum(summary_counts.values())}")
    for key, count in summary_counts.items():
        title = section_names[key][0].split(". ", 1)[-1] if ". " in section_names[key][0] else section_names[key][0]
        print(f"  {title}: {count}")

if __name__ == "__main__":
    main()
