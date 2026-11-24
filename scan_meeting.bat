@echo off & chcp 65001 >nul & py -3.12 -x "%~f0" %* & pause & exit /b
import hashlib
import os
import subprocess
import sys
import urllib.parse
from pathlib import Path

DEFAULT_OWNER = "ImaterialC"
DEFAULT_REPO = "Misora-Reference"
DEFAULT_BRANCH = "main"

DEFAULT_MAX_LINES = 1500
DEFAULT_MAX_KB = 65

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
    safe_name = target.name.replace(" ", "_")
    for old in target.glob(f"_BUNDLE_{safe_name}*.md"):
        try:
            old.unlink()
        except OSError:
            pass

    segments = []
    for fp in files:
        if fp.suffix.lower() not in TEXT_BUNDLE_EXTS:
            continue
        raw_bytes = fp.read_bytes()
        sha = hashlib.sha256(raw_bytes).hexdigest()
        rel = fp.relative_to(repo_root).as_posix()
        text = raw_bytes.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
        all_lines = text.splitlines()

        eff_max_lines = max(50, max_lines - 10)
        eff_max_bytes = max(4096, max_bytes - 512)

        block = f"--- FILE: {rel} | L:{len(all_lines)} | SHA:{sha[:12]} ---\n{text.rstrip()}\n\n"
        b_bytes = len(block.encode("utf-8"))
        b_lines = block.count("\n")
        if b_lines <= max_lines and b_bytes <= max_bytes:
            segments.append((rel, block, b_lines, b_bytes))
        else:
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
                seg_header = f"--- FILE: {rel} [PART {sub_idx} | L{start_ln}-{end_ln}/{len(all_lines)} | SHA:{sha[:12]}] ---\n"
                seg_body = "\n".join(chunk_lines).rstrip() + "\n\n"
                full_seg = seg_header + seg_body
                segments.append((rel, full_seg, full_seg.count("\n"), len(full_seg.encode("utf-8"))))
                sub_idx += 1

    buckets = []
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
        top_banner = f"# BUNDLE {target.name} ({part_no}/{total_parts}) | Files: {', '.join(included_names)}\n\n"
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
        print("=" * 60)
        print("  MISORA-REFERENCE — SCANNER & SAFE BUNDLER")
        print("=" * 60)
        print(f"Repo: {owner}/{repo} ({branch}) | Root: {repo_root}\n")
        print("[0] SEMUA FOLDER")
        for idx, d in enumerate(subdirs, 1):
            print(f"[{idx}] {d.name}")
        choice = input("\nPilih nomor (Enter = semua): ").strip()
        target = repo_root if (not choice or choice == "0") else subdirs[int(choice) - 1]

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
        print("Tidak ada file teks di:", target)
        return

    max_lines = DEFAULT_MAX_LINES
    max_kb = DEFAULT_MAX_KB
    if sys.stdin.isatty():
        make_bundle = input("\nBuat bundle (_BUNDLE_*.md)? [Y/n]: ").strip().lower()
        do_bundle = (make_bundle != "n")
        if do_bundle:
            ml_in = input(f"Maks baris/bundle [Enter={DEFAULT_MAX_LINES}]: ").strip()
            if ml_in.isdigit() and int(ml_in) >= 200:
                max_lines = int(ml_in)
            mk_in = input(f"Maks KB/bundle [Enter={DEFAULT_MAX_KB}]: ").strip()
            if mk_in.isdigit() and int(mk_in) >= 16:
                max_kb = int(mk_in)
    else:
        do_bundle = True

    bundle_entries = build_chunked_bundles(target, repo_root, files, max_lines, max_kb * 1024) if do_bundle else []

    lines = [
        f"# INDEX `{target.name}` ({owner}/{repo}@{branch}, {len(files)} files)",
        "",
    ]

    bundle_clip_lines = []
    if bundle_entries:
        lines.append(f"## Bundles (max {max_lines}L / {max_kb}KB)")
        lines.append("| Bundle | Lines | Bytes | SHA12 | URL |")
        lines.append("| :--- | ---: | ---: | :--- | :--- |")
        for b_path, b_lines, b_size, b_sha in bundle_entries:
            rel_b = b_path.relative_to(repo_root).as_posix()
            url_b = make_raw_url(owner, repo, branch, rel_b)
            lines.append(f"| `{rel_b}` | {b_lines} | {b_size} | `{b_sha[:12]}` | {url_b} |")
            bundle_clip_lines.append(f"- `{rel_b}` ({b_lines}L, {b_size}B, `{b_sha[:12]}`)\n  {url_b}")
        lines.append("")

    lines.append("## Files")
    lines.append("| File | Lines | Bytes | SHA12 | Flag | URL |")
    lines.append("| :--- | ---: | ---: | :--- | :--- | :--- |")

    plain_urls = []
    for fp in files:
        raw_bytes = fp.read_bytes()
        sha = hashlib.sha256(raw_bytes).hexdigest()
        line_cnt = raw_bytes.decode("utf-8", errors="replace").count("\n") + 1
        rel = fp.relative_to(repo_root).as_posix()
        url = make_raw_url(owner, repo, branch, rel)
        flag = "LARGE" if (line_cnt > max_lines or len(raw_bytes) > max_kb * 1024) else "OK"
        lines.append(f"| `{rel}` | {line_cnt} | {len(raw_bytes)} | `{sha[:12]}` | {flag} | {url} |")
        plain_urls.append(f"- `{rel}` ({line_cnt}L, {len(raw_bytes)}B, `{sha[:12]}`)\n  {url}")

    out_index = target / "MANIFEST_AUTO.md"
    out_index.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    idx_url = make_raw_url(owner, repo, branch, out_index.relative_to(repo_root).as_posix())

    print(f"\n[OK] Index : {out_index}")
    for b_path, b_lines, b_size, _ in bundle_entries:
        print(f"[OK] Bundle: {b_path.name} ({b_lines}L, {b_size}B)")

    bundle_section = ("Bundles:\n" + "\n".join(bundle_clip_lines) + "\n\n") if bundle_clip_lines else ""
    clipboard_block = (
        f"Index: {idx_url}\n\n"
        f"{bundle_section}"
        f"Files ({len(files)}):\n" + "\n".join(plain_urls) + "\n"
    )

    if copy_to_clipboard(clipboard_block):
        print("\n[OK] URL disalin ke Clipboard! Tinggal push & Ctrl+V.")
    else:
        print("\n" + clipboard_block)


if __name__ == "__main__":
    main()
