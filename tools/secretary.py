#!/usr/bin/env python3
"""
Secretary Assistant CLI Tool for Multi-AI Engineering Review Repositories.
Automates ingestion of new chat transcripts, archive compression, integrity checks, and status reporting.
"""

import argparse
import hashlib
import os
import sys
import zipfile


def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def cmd_status(args):
    print("=" * 60)
    print("SECRETARY STATUS REPORT — REFERENCE REPOSITORY")
    print("=" * 60)

    # Active Documents
    print("\n[ACTIVE DOCUMENTS]")
    for doc in ["README.md", "SUMMARY_AND_CONSENSUS.md", "INSTANT_ONBOARDING_PROMPT.md", "SECRETARY_PLAYBOOK.md"]:
        if os.path.exists(doc):
            sz = os.path.getsize(doc)
            print(f"  ✓ {doc:<30} ({sz/1024:.1f} KB)")
        else:
            print(f"  ✗ {doc:<30} (MISSING)")

    # Prompts
    print("\n[PROMPTS]")
    if os.path.exists("prompts"):
        for f in sorted(os.listdir("prompts")):
            p = os.path.join("prompts", f)
            print(f"  ✓ {f:<30} ({os.path.getsize(p)/1024:.1f} KB)")
    else:
        print("  (None)")

    # Decisions
    print("\n[DECISION RECORDS]")
    if os.path.exists("decisions"):
        for f in sorted(os.listdir("decisions")):
            p = os.path.join("decisions", f)
            print(f"  ✓ {f:<30} ({os.path.getsize(p)/1024:.1f} KB)")
    else:
        print("  (None)")

    # Archives
    print("\n[COLD ARCHIVES]")
    if os.path.exists("archives"):
        for f in sorted(os.listdir("archives")):
            if f.endswith(".zip"):
                p = os.path.join("archives", f)
                sz = os.path.getsize(p)
                print(f"  📦 {f:<30} ({sz/1024:.1f} KB)")
    else:
        print("  (None)")
    print("=" * 60)


def cmd_verify_zips(args):
    print("Running integrity checks on all archives...")
    if not os.path.exists("archives"):
        print("No archives/ directory found.")
        return 0

    all_passed = True
    for f in sorted(os.listdir("archives")):
        if f.endswith(".zip"):
            p = os.path.join("archives", f)
            try:
                with zipfile.ZipFile(p, "r") as zf:
                    corrupt = zf.testzip()
                    if corrupt is None:
                        count = len(zf.namelist())
                        print(f"  ✓ {f}: PASS ({count} files, {os.path.getsize(p)/1024:.1f} KB)")
                    else:
                        print(f"  ✗ {f}: CORRUPT (First bad file: {corrupt})")
                        all_passed = False
            except Exception as e:
                print(f"  ✗ {f}: FAILED TO OPEN ({e})")
                all_passed = False

    return 0 if all_passed else 1


def cmd_ingest(args):
    filepath = args.file
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return 1

    print(f"Ingesting transcript '{filepath}' ({os.path.getsize(filepath):,} bytes)...")
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    print(f"Total lines: {len(lines):,}")

    # Inspect headers
    headers = [line.strip() for line in lines if line.startswith("# ") or line.startswith("## ")]
    print(f"Found {len(headers)} top-level markdown headers.")
    for h in headers[:10]:
        print(f"  {h}")
    if len(headers) > 10:
        print(f"  ... and {len(headers)-10} more headers")

    # Look for LOCK keywords
    locks = [line.strip() for line in lines if "LOCK" in line and len(line.strip()) < 100]
    print(f"\nPotential LOCK keywords found ({len(locks)}):")
    for l in locks[:5]:
        print(f"  -> {l}")

    return 0


def main():
    parser = argparse.ArgumentParser(description="Secretary Assistant CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # status
    p_status = subparsers.add_parser("status", help="Show active vs archived repository status")
    p_status.set_defaults(func=cmd_status)

    # verify-zips
    p_verify = subparsers.add_parser("verify-zips", help="Verify integrity of all zip archives")
    p_verify.set_defaults(func=cmd_verify_zips)

    # ingest
    p_ingest = subparsers.add_parser("ingest", help="Analyze and inspect a new chat transcript")
    p_ingest.add_argument("file", help="Path to transcript file")
    p_ingest.set_defaults(func=cmd_ingest)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main() or 0)
