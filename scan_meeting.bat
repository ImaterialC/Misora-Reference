@echo off & chcp 65001 >nul & py -3.12 -x "%~f0" %* & pause & exit /b
import hashlib
import os
import subprocess
import sys
import urllib.parse
from pathlib import Path

# === KONFIGURASI DEFAULT (auto-detect dari git remote & branch jika ada) ===
DEFAULT_OWNER = "ImaterialC"
DEFAULT_REPO = "Misora-Reference"
DEFAULT_BRANCH = "main"

DEFAULT_MAX_LINES = 1500   # Batas aman anti-terpotong untuk mayoritas AI web-fetch
DEFAULT_MAX_KB = 65        # Batas aman ukuran per file bundle (~65 KB)

IGNORE_DIRS = {".git", ".agents", "__pycache__", ".vscode", "node_modules", "split_output"}
IGNORE_EXTS = {".bat", ".exe", ".pyc", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".zip", ".7z"}
IGNORE_NAMES = {".gitkeep", ".DS_Store", "Thumbs.db", "MANIFEST_AUTO.md"}
TEXT_BUNDLE_EXTS = {".md", ".txt", ".json", ".yaml", ".yml", ".sha256", ".py", ".csv", ".ini"}


def detect_git_info(repo_root: Path):
    owner, repo, branch = DEFAULT_OWNER, DEFAULT_REPO, DEFAULT_BRANCH
    try:
        url = subprocess.check_output(
            ["git", "-C", str(repo_root), "config", "--get", "remote.origin.url"],
            text=True, stderr=subprocess.DEVNULL
        ).strip()
        if "github.com" in url:
            tail = url.split("github.com")[-1].lstrip(":/").removesuffix(".git")
            parts = tail.split("/")
            if len(parts) >= 2:
                owner, repo = parts[0], parts[1]
        br = subprocess.check_output(
            ["git", "-C", str(repo_root), "rev-parse", "--abbrev-ref", "HEAD"],
            text=True, stderr=subprocess.DEVNULL
        ).strip()
        if br and br != "HEAD":
            branch = br
    except Exception:
        pass
    return owner, repo, branch


def find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for p in [cur, *cur.parents]:
        if (p / ".git").exists():
            return p
    return cur


def make_raw_url(owner: str, repo: str, branch: str, rel_posix: str) -> str:
    encoded = "/".join(urllib.parse.quote(part) for part in rel_posix.split("/"))
    return f"https://raw.githubusercontent.com/{owner}/{repo}/refs/heads/{branch}/{encoded}"


def copy_to_clipboard(text: str) -> bool:
    if os.name != "nt":
        return False
    try:
        subprocess.run(
            [
                "powershell", "-NoProfile", "-Command",
                "[Console]::InputEncoding = [Text.Encoding]::UTF8; "
                "Set-Clipboard -Value ([Console]::In.ReadToEnd())"
            ],
            input=text.encode("utf-8"),
            check=True,
        )
        return True
    except Exception:
        return False


def build_chunked_bundles(
    target: Path,
    repo_root: Path,
    files: list[Path],
    max_lines: int,
    max_bytes: int,
) -> list[tuple[Path, int, int, str]]:
    """Bundle text files into 1+ parts that never exceed max_lines or max_bytes."""
    safe_name = target.name.replace(" ", "_")

    # Hapus bundle lama di folder target agar tidak ada sisa part usang
    for old in target.glob(f"_BUNDLE_{safe_name}*.md"):
        try:
            old.unlink()
        except OSError:
            pass

    # Siapkan segmen-segmen teks (jika 1 file sendiri > max_lines/max_bytes, pecah aman per baris)
    segments = []  # list of (rel_path, seg_text, seg_lines, seg_bytes)
    for fp in files:
        if fp.suffix.lower() not in TEXT_BUNDLE_EXTS:
            continue
        raw_bytes = fp.read_bytes()
        sha = hashlib.sha256(raw_bytes).hexdigest()
        rel = fp.relative_to(repo_root).as_posix()
        text = raw_bytes.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
        all_lines = text.splitlines()

        header_budget = 10
        eff_max_lines = max(50, max_lines - header_budget)
        eff_max_bytes = max(4096, max_bytes - 512)

        # Cek apakah muat utuh dalam 1 segmen
        block = (
            f"{'=' * 70}\n"
            f"FILE: {rel} | LINES: {len(all_lines)} | SIZE: {len(raw_bytes)} B | SHA-256: {sha}\n"
            f"{'=' * 70}\n"
            f"{text.rstrip()}\n\n"
        )
        b_bytes = len(block.encode("utf-8"))
        b_lines = block.count("\n")
        if b_lines <= max_lines and b_bytes <= max_bytes:
            segments.append((rel, block, b_lines, b_bytes))
        else:
            # Pecah file besar ini secara aman per rentang baris asli
            idx = 0
            sub_idx = 1
            while idx < len(all_lines):
                chunk_lines = []
                chunk_bytes = 0
                start_ln = idx + 1
                while idx < len(all_lines) and len(chunk_lines) < eff_max_lines:
                    ln_str = all_lines[idx] + "\n"
                    ln_b = len(ln_str.encode("utf-8"))
                    if chunk_lines and (chunk_bytes + ln_b > eff_max_bytes):
                        break
                    chunk_lines.append(all_lines[idx])
                    chunk_bytes += ln_b
                    idx += 1
                end_ln = start_ln + len(chunk_lines) - 1
                seg_header = (
                    f"{'=' * 70}\n"
                    f"FILE: {rel} [CHUNK {sub_idx} | ORIG LINES {start_ln}-{end_ln} / {len(all_lines)}] | SHA-256(full): {sha[:16]}\n"
                    f"{'=' * 70}\n"
                )
                seg_body = "\n".join(chunk_lines).rstrip() + "\n\n"
                full_seg = seg_header + seg_body
                segments.append((rel, full_seg, full_seg.count("\n"), len(full_seg.encode("utf-8"))))
                sub_idx += 1

    # Gabungkan segmen ke dalam part-part bundle
    buckets = []  # list of list of segments
    cur_bucket = []
    cur_lines = 0
    cur_bytes = 0
    for seg in segments:
        _, _, s_lines, s_bytes = seg
        if cur_bucket and (cur_lines + s_lines > max_lines or cur_bytes + s_bytes > max_bytes):
            buckets.append(cur_bucket)
            cur_bucket = [seg]
            cur_lines = s_lines
            cur_bytes = s_bytes
        else:
            cur_bucket.append(seg)
            cur_lines += s_lines
            cur_bytes += s_bytes
    if cur_bucket:
        buckets.append(cur_bucket)

    created = []
    total_parts = len(buckets)
    for part_no, bucket in enumerate(buckets, 1):
        if total_parts == 1:
            b_path = target / f"_BUNDLE_{safe_name}.md"
        else:
            b_path = target / f"_BUNDLE_{safe_name}_part{part_no:02d}of{total_parts:02d}.md"

        included_names = sorted({s[0] for s in bucket})
        top_banner = (
            f"# COMBINED BUNDLE: {target.name} (Part {part_no}/{total_parts})\n"
            f"# Limits: max {max_lines} lines / {max_bytes // 1024} KB per part | Files in this part: {len(included_names)}\n"
            f"# Included: {', '.join(included_names)}\n\n"
        )
        content = top_banner + "".join(s[1] for s in bucket)
        raw_out = content.encode("utf-8")
        b_path.write_bytes(raw_out)
        created.append((b_path, content.count("\n"), len(raw_out), hashlib.sha256(raw_out).hexdigest()))

    return created


def main():
    script_dir = Path(__file__).resolve().parent
    repo_root = find_repo_root(script_dir)
    owner, repo, branch = detect_git_info(repo_root)

    if len(sys.argv) > 1:
        target = Path(sys.argv[1]).resolve()
    else:
        subdirs = sorted([
            d for d in repo_root.iterdir()
            if d.is_dir() and d.name not in IGNORE_DIRS and not d.name.startswith(".")
        ])
        print("=" * 64)
        print("  MISORA-REFERENCE — AUTO MEETING SCANNER & SAFE BUNDLER")
        print("=" * 64)
        print(f"Repo terdeteksi : {owner}/{repo} (branch: {branch})")
        print(f"Root folder     : {repo_root}\n")
        print("[0] SCAN SEMUA FOLDER (Root + semua sub-folder)")
        for idx, d in enumerate(subdirs, 1):
            print(f"[{idx}] {d.name}")
        choice = input("\nPilih nomor folder (Enter = semua): ").strip()
        if not choice or choice == "0":
            target = repo_root
        else:
            target = subdirs[int(choice) - 1]

    files = []
    for root, dirs, filenames in os.walk(target):
        dirs[:] = sorted([d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")])
        for fn in sorted(filenames):
            if fn in IGNORE_NAMES or fn.startswith("_BUNDLE_"):
                continue
            fp = Path(root) / fn
            if fp.suffix.lower() in IGNORE_EXTS:
                continue
            files.append(fp)

    if not files:
        print("Tidak ada file referensi teks ditemukan di:", target)
        return

    max_lines = DEFAULT_MAX_LINES
    max_kb = DEFAULT_MAX_KB
    if sys.stdin.isatty():
        make_bundle = input("\nBuat file bundle anti-terpotong (_BUNDLE_*.md)? [Y/n]: ").strip().lower()
        do_bundle = (make_bundle != "n")
        if do_bundle:
            ml_in = input(f"Batas maksimal baris per bundle [Enter = {DEFAULT_MAX_LINES}]: ").strip()
            if ml_in.isdigit() and int(ml_in) >= 200:
                max_lines = int(ml_in)
            mk_in = input(f"Batas maksimal KB per bundle [Enter = {DEFAULT_MAX_KB}]: ").strip()
            if mk_in.isdigit() and int(mk_in) >= 16:
                max_kb = int(mk_in)
    else:
        do_bundle = True

    bundle_entries = []
    if do_bundle:
        bundle_entries = build_chunked_bundles(target, repo_root, files, max_lines, max_kb * 1024)

    lines = [
        f"# MEETING REFERENCE INDEX — `{target.name}`",
        f"Repo: `https://github.com/{owner}/{repo}` | Branch: `{branch}` | Files: {len(files)}",
        "",
    ]

    bundle_clip_lines = []
    if bundle_entries:
        lines.append(f"## Safe Chunked Bundles (max {max_lines} lines / {max_kb} KB per part)")
        lines.append("| Bundle Part | Lines | Size | SHA-256 (12) | Raw URL |")
        lines.append("| :--- | ---: | ---: | :--- | :--- |")
        for b_path, b_lines, b_size, b_sha in bundle_entries:
            rel_b = b_path.relative_to(repo_root).as_posix()
            url_b = make_raw_url(owner, repo, branch, rel_b)
            lines.append(f"| `{rel_b}` | {b_lines} | {b_size} B | `{b_sha[:12]}` | {url_b} |")
            bundle_clip_lines.append(f"- `{rel_b}` ({b_lines} lines, {b_size} B, sha256:`{b_sha[:12]}`)\n  {url_b}")
        lines.append("")

    lines.append("## Individual Source Files")
    lines.append("| File | Lines | Size | SHA-256 (12) | Note | Raw URL |")
    lines.append("| :--- | ---: | ---: | :--- | :--- | :--- |")

    plain_urls = []
    for fp in files:
        raw_bytes = fp.read_bytes()
        sha = hashlib.sha256(raw_bytes).hexdigest()
        line_cnt = raw_bytes.decode("utf-8", errors="replace").count("\n") + 1
        rel = fp.relative_to(repo_root).as_posix()
        url = make_raw_url(owner, repo, branch, rel)
        note = "LARGE (use bundle/split)" if (line_cnt > max_lines or len(raw_bytes) > max_kb * 1024) else "OK"
        lines.append(f"| `{rel}` | {line_cnt} | {len(raw_bytes)} B | `{sha[:12]}` | {note} | {url} |")
        plain_urls.append(f"- `{rel}` ({line_cnt} lines, {len(raw_bytes)} B, sha256:`{sha[:12]}`)\n  {url}")

    out_index = target / "MANIFEST_AUTO.md"
    out_index.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    rel_idx = out_index.relative_to(repo_root).as_posix()
    idx_url = make_raw_url(owner, repo, branch, rel_idx)

    print(f"\n[OK] Tersimpan index : {out_index}")
    print(f"     Raw URL index   : {idx_url}")
    for b_path, b_lines, b_size, _ in bundle_entries:
        print(f"[OK] Tersimpan bundle: {b_path.name} ({b_lines} lines, {b_size} B)")

    bundle_section = ""
    if bundle_clip_lines:
        bundle_section = (
            f"\nSafe Chunked Bundle(s) (max {max_lines} lines / {max_kb} KB):\n"
            + "\n".join(bundle_clip_lines)
            + "\n"
        )

    clipboard_block = (
        f"Reference Index for `{target.name}` (push ke GitHub dulu sebelum kirim ke AI):\n"
        f"- Index: {idx_url}\n"
        f"{bundle_section}\n"
        f"Individual Raw URLs ({len(files)} files):\n"
        + "\n".join(plain_urls)
        + "\n"
    )

    if copy_to_clipboard(clipboard_block):
        print("\n[OK] Daftar URL + SHA-256 sudah otomatis DISALIN ke Clipboard! Tinggal Ctrl+V.")
    else:
        print("\n--- COPY BLOK DI BAWAH INI ---\n")
        print(clipboard_block)


if __name__ == "__main__":
    main()
