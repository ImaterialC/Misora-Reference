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

    # Active Debates
    print("\n[ACTIVE DEBATES]")
    if os.path.exists("active_debates"):
        debates = [d for d in sorted(os.listdir("active_debates")) if os.path.isdir(os.path.join("active_debates", d))]
        if debates:
            for d in debates:
                p = os.path.join("active_debates", d)
                files_cnt = len(os.listdir(p))
                print(f"  🟢 {d:<30} ({files_cnt} files in session)")
        else:
            print("  (None active)")
    else:
        print("  (None active)")

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
    archive_dirs = ["archives", os.path.join("reference_toolchains", "archives")]
    found_archives = False
    for adir in archive_dirs:
        if os.path.exists(adir):
            for f in sorted(os.listdir(adir)):
                if f.endswith(".zip"):
                    p = os.path.join(adir, f)
                    sz = os.path.getsize(p)
                    print(f"  📦 {p:<45} ({sz/1024:.1f} KB)")
                    found_archives = True
    if not found_archives:
        print("  (None)")

    # Reference Toolchains Desk
    print("\n[REFERENCE TOOLCHAINS (ACTIVE DESK)]")
    rt_docs = [
        os.path.join("reference_toolchains", "README.md"),
        os.path.join("reference_toolchains", "PROGRAM_LINEAGE_AND_ALIASES.md"),
        os.path.join("reference_toolchains", "EXTRACTOR_PLUGIN_PROPOSAL.md"),
        os.path.join("reference_toolchains", "community_heritage", "HERITAGE_AND_SOURCES.md"),
    ]
    for doc in rt_docs:
        if os.path.exists(doc):
            sz = os.path.getsize(doc)
            print(f"  ✓ {doc:<45} ({sz/1024:.1f} KB)")

    v3_path = os.path.join("reference_toolchains", "v3_kyouka_suite")
    if os.path.exists(v3_path):
        v3_files = [f for root, _, files in os.walk(v3_path) for f in files]
        print(f"  🟢 V3 Kyouka Suite: {len(v3_files)} files active (uncompressed)")

    v2_path = os.path.join("reference_toolchains", "v2_modular_tools")
    if os.path.exists(v2_path):
        v2_files = [f for root, _, files in os.walk(v2_path) for f in files]
        print(f"  🟢 V2 Modular Tools: {len(v2_files)} files active (uncompressed)")

    print("=" * 60)


def cmd_verify_zips(args):
    print("Running integrity checks on all archives...")
    archive_dirs = ["archives", os.path.join("reference_toolchains", "archives")]
    all_passed = True
    found_any = False

    for adir in archive_dirs:
        if not os.path.exists(adir):
            continue
        for f in sorted(os.listdir(adir)):
            if f.endswith(".zip"):
                found_any = True
                p = os.path.join(adir, f)
                try:
                    with zipfile.ZipFile(p, "r") as zf:
                        corrupt = zf.testzip()
                        if corrupt is None:
                            count = len(zf.namelist())
                            print(f"  ✓ {p}: PASS ({count} files, {os.path.getsize(p)/1024:.1f} KB)")
                        else:
                            print(f"  ✗ {p}: CORRUPT (First bad file: {corrupt})")
                            all_passed = False
                except Exception as e:
                    print(f"  ✗ {p}: FAILED TO OPEN ({e})")
                    all_passed = False

    if not found_any:
        print("No zip archives found.")

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
