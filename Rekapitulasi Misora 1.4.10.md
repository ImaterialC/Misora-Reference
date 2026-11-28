### 1. Catatan Penting: Log PowerShell yang Ditempel Masih Log `T-02`

Log PowerShell di atas adalah commit **`T-02`** sebelumnya (`fb6088e` + `3edf43e`), bukan commit **`DOCS-01`** (`AGENTS.md`, `PROJECT_STATE.md`, `docs/project/OPEN_ISSUES.md` + `T-02_Walkthrough.md`).

Sebelum menjalankan `/plan` berikutnya di Antigravity, cek cepat apakah **`DOCS-01`** sudah benar-benar di-commit & di-push di kedua repo (setelah mendapat *final clearance* Rev 3 dari GPT-6):

```powershell
git -C D:\Misora-Editor log -1 --oneline
git -C D:\Misora-Editor status --short --untracked-files=all
git -C D:\Reference\Misora-Reference log -1 --oneline
git -C D:\Reference\Misora-Reference status --short --untracked-files=all

```

Jika `DOCS-01` belum dijalankan/di-commit, selesaikan dulu `DOCS-01` agar `/plan` **`T-08a`** membaca `AGENTS.md`, `PROJECT_STATE.md`, dan `OPEN_ISSUES.md` yang sudah sinkron.

---

### 2. Penjabaran Audit Rencana Final (Untuk Catatan Project Lead)

Rencana di bawah adalah konsensus akhir **Opsi A** hasil audit 3 AI (Gemini, GPT-6, Qwen) pada baseline produk **`v1.4.15`** (`v1.5.0` tetap **`CANCELLED / NOT RELEASED / VERSION PROMOTION NOT AUTHORIZED`**). Seluruh fase setelah `DOCS-01` berstatus **urutan perencanaan (*planning order*), bukan izin implementasi**.

#### A. Status Baseline & Pekerjaan Selesai

* **`ENV-01` (Context Hygiene Kit v2):** Selesai di baseline historis `648cb52...` (arsip mentah, `AGENTS.md`, `PROJECT_STATE.md`, `CONTEXT_ROUTER.md`, `MISORA_SYMBOL_INDEX.md`).


* **`T-01` (`BUG-UI-EMPTY-STATE-01`):** **`HISTORICAL-REFERENCE`** (Tertutup) — 8 penggantian `winfo_ismapped()` → `winfo_manager() == "pack"`, 11/11 tes baru `PASS`, Manual QA Windows `M-1..M-12` `PASS` (`8b75b9e`).
* **`T-02` (`u-08`):** **`APPROVED FOR CLOSEOUT`** → **`HISTORICAL-REFERENCE`** di `DOCS-01` — tooltip `lbl_char_overflow` dinamis `54d x 3` + kalimat *dual-font* (`fb6088e` + indeks simbol `3edf43e`), 8/8 tes baru `PASS`, total suite **`494 = 451 PASS + 35 SKIP + 6 FAIL + 2 ERROR`** (`0` regresi), Manual QA `M-1..M-4` `PASS` (M-1/M-2 verifikasi 2 baris & DPI; M-3 Next/Prev utuh; M-4 verifikasi teks lengkap verbatim + indikator merah `54/54d · 1/3L`).



#### B. Peta Urutan Update Final (Opsi A — Disepakati Panel AI)

| Fase | Tiket | Status Bukti | Fokus & Syarat Kunci Hasil Audit |
| --- | --- | --- | --- |
| **Fase 0** | **`DOCS-01`** | Docs-Only | Tutup `T-02`, hapus instruksi lama `ENV-01` & gate `475` di `PROJECT_STATE.md`, ganti `50 -> 54` di `AGENTS.md` §7 baris 40 (cap `<= 6,144` byte), perbarui deskripsi faktual `T-03`, log `T-08a`/`T-08b`/`T-06b`/`T-13`, sinkronkan `T-02_Walkthrough.md`. Nol `.py`.

 |
| **Fase 1a** | **`T-08a`** (`BUG-UI-TOOLTIP-CLIP-01`) | `CONFIRMED` (Windows 100%/125% DPI) · `ROOT-CAUSE: NEEDS-CODE-VERIFY` | **Micro-fix independen** pada kelas `ToolTip`: *screen-edge clamping* sumbu **X dan Y**, ukur `reqwidth/reqheight` sebelum memposisikan, dukung *work area*/taskbar, DPI 100%/125%, dan *multi-monitor* (termasuk koordinat negatif). Prasyarat wajib sebelum `T-07`.

 |
| **Fase 1b** | **`T-04`** (`u-02`) | `REPORTED + NEEDS-REPRO` | Marker merah overflow untuk baris ke-4+ (`>3L`, *hard linebreak* / aturan lebar terender) + **audit perilaku numerator `54/54d` merah** (temuan `M-4` `T-02`: apakah angka mentok/di-clamp di `54` atau persis di batas, karena `54/54d` merah bertentangan dengan tooltip `<= 54`).

 |
| **Fase 2a** | **`T-03`** (`u-05`) | `CONFIRMED` (8 repro Windows, 4 screenshot) · `ROOT-CAUSE: NEEDS-CODE-VERIFY` | Susun **1 Kontrak State Visual All Script** dulu (Active Focus, Hover, Selected, Locked harus ortogonal & diturunkan murni dari data, satu jalur repaint penuh). Lalu perbaiki bug *stale purple highlight* saat `Next/Prev`, shortcut, atau `Pin` (Pin OFF & Select Box OFF) sampai hanya 1 kartu aktif yang tersorot.

 |
| **Fase 2b** | **`T-10`** (`u-06`) | `PROPOSAL` | Tambah kanal visual *Hover* & *Selected Box* secara terpisah di atas kontrak Fase 2a tanpa merusak performa *virtualized card pool*. Sengaja dipisah dari 2a agar regresi bugfix vs fitur tidak bercampur.

 |
| **Fase 3a** | **`T-08b`** (`BUG-UI-SNAP-HALF-CLIP-01`) | `CONFIRMED` (~960px snap-half) · `ROOT-CAUSE: NEEDS-CODE-VERIFY` | Pulihkan keterjangkauan tombol keselamatan data (**`Save File / Patch Bundle`** & **`Revert Box`**) serta checkbox `All Script`/`Preview` pada lebar ~960px. Cek konflik `minsize(980, 620)` dan urutan `pack`.

 |
| **Fase 3b–3c** | **`T-08`** (`u-11`) & **`T-09`** (`u-12`) | `PROPOSAL` | Redesain ribbon responsif (pisahkan indikator `x/54d · y/3L Box a/b` agar `Prev/Next` tidak bergeser; evaluasi 4-baris vs kompak & toggle menu View) + kontrol seleksi eksplisit Insert/Replace/tri-state Select All (cek duplikasi dengan S11e). Wajib *design sign-off* sebelum kode.

 |
| **Fase 4** | **`T-05`**, **`T-06`**, **`T-06b`** | `PROPOSAL` (kecuali perilaku close `T-06b` = `REPORTED + NEEDS-REPRO`) | Pisah 3 folder path (Game / RedirectedResources / XUAT Text tanpa hardcode framework), direktori simpan terpisah `.misora` vs bundle, dan dialog tutup aplikasi terpadu. **Wajib verifikasi dulu:** (1) apakah `_on_app_exit` masih punya risiko *data loss* `F-GPT-03` (hanya simpan file aktif), dan (2) apakah format `.misora` sudah eksis di `v1.4.15`.

 |
| **Fase 5** | **`T-07`** (`u-07`) | `PROPOSAL` | Perluasan tooltip 350 ms ke label informatif non-tombol (dikerjakan **setelah** `T-08a` & layout ribbon `T-08`/`T-09` stabil).

 |
| **Fase 6 (Track B & Maintenance)** | **Test Hygiene + `T-11` → `T-13` + `T-12` + `T-14**` | `PROPOSAL` / `DEFERRED` | • **Test Hygiene:** 3 *non-fixture fail* + docstring `test_v15_s02_fonts_ruler_metrics.py:253` (`"50x3"`) + pemulihan 35 SKIP / 3 FAIL / 2 ERROR jika `storydata_1001005.unity3d` tersedia.<br>

<br>• **`T-11` → `T-13` (Wajib Berurutan):** `T-11` membangun *Original Source Snapshot* persisten + *provenance* saat tangkap (`datamine` vs `plugin`) + **key stabil lintas sesi (DILARANG pakai `Record.uid`/`Box.uid` runtime)**; baru `T-13` membangun *append-only Commit Archive* `Original_X=Committed_Y` khusus entri berubah saat patch sukses.<br>

<br>• **`T-12`:** Async worker thread untuk sinkronisasi XUAT.<br>

<br>• **`T-14`:** GitHub Actions release `.zip`/`.exe`.

 |

#### C. Dua *Priority Watch* (Bisa Menggeser Urutan Jika Terbukti)

1. **`F-GPT-07` (`XUAT-JP-KEY-DRIFT`):** Status di `v1.4.15` belum diverifikasi — jika drift masih terjadi setelah save pertama, **`T-11` naik menjadi P1 *data correctness*** dan harus dimajukan sebelum pekerjaan UI.


2. **`F-GPT-03` (`EXIT-SAVES-ONLY-ACTIVE`):** Saat mengaudit `_on_app_exit` untuk `T-06b`, jika menutup aplikasi dengan banyak file *dirty* ternyata hanya menyimpan file aktif, perbaikan *exit safety* naik prioritas lebih awal.



---

### 3. Prompt `/plan` Berikutnya — Fase 1a: `T-08a` (`BUG-UI-TOOLTIP-CLIP-01` — ToolTip Boundary Clamping)

Jalankan prompt ini di **chat baru** Antigravity pada `D:\Misora-Editor` **setelah commit `DOCS-01` selesai dan *working tree* bersih** (jika nanti Anda memilih menukar 1a/1b untuk mengerjakan `T-04` lebih dulu, beri tahu saya):

```text
/plan Investigate and prepare a minimal, root-cause-proven implementation plan for T-08a (`BUG-UI-TOOLTIP-CLIP-01` — ToolTip screen-edge clipping) using the ENV-01 layered context workflow.

CONTEXT LOADING (ENV-01 LAYERED POLICY — DO NOT LOAD ARCHIVES OR FULL 1 MB misora.py):
- Layer 0 (Always): @AGENTS.md @PROJECT_STATE.md
- Layer 1 (Task-Specific via Router): @docs/ai/CONTEXT_ROUTER.md @docs/project/OPEN_ISSUES.md @docs/architecture/MISORA_SYMBOL_INDEX.md
- Layer 2 (Targeted Source & Tests ONLY): Use MISORA_SYMBOL_INDEX.md + narrow grep on `misora.py` (and `tests/`) to read ONLY:
  * Class `ToolTip` (all methods: `__init__`, `show_tip`, `hide_tip`, positioning/geometry logic, `create_tooltip`)
  * Any existing monitor/work-area/DPI helper functions in `misora.py` (read-only check; honor AGENTS.md Rule 23 — NEVER modify runtime DPI awareness)
  * `tests/test_t02_next_tooltip.py` and `tests/test_v15_s11e_polish_splash_menu_tooltips.py` (narrow read-only reference).
- Layer 3 (Archives): DO NOT load `docs/archive/`.

==================================================
PART 0 — EXECUTION MODE & NON-NEGOTIABLE GUARDRAILS
==================================================
1. Planning-First Gate (STRICTLY READ-ONLY IN D:\Misora-Editor):
   - Do NOT create, modify, or delete ANY file inside `D:\Misora-Editor` during `/plan`.
   - Write (or overwrite in-place) the complete plan artifact ONLY outside the worktree at:
     `D:\Reference\Misora-Reference\T-08a_Implementation_Plan.md`
     (Report the written path and its SHA-256 hash, then STOP — WAITING FOR INDEPENDENT REVIEW.)
2. Prerequisite Gate (DOCS-01 MUST BE COMMITTED FIRST):
   - Verify `AGENTS.md` §7 already reads `54 digit-widths` and `docs/project/OPEN_ISSUES.md` already contains `T-08a` (`BUG-UI-TOOLTIP-CLIP-01`). If NOT, STOP immediately and report that DOCS-01 is not yet committed.
3. Evidence Discipline:
   - T-08a visual symptom is `CONFIRMED` on Windows 11 (100% & 125% DPI maximized, `lbl_char_overflow` tooltip clipped past the right screen edge), while `ROOT-CAUSE` is `NEEDS-CODE-VERIFY`.
   - Quote the EXACT live `file:line` code of `ToolTip` in `misora.py` (NO guessed method names or line numbers) and run a read-only probe on a genuine `MisoraApp` instance (`CONFIG_PATH` patched to temp dir) proving the exact un-clamped `(x, y, reqwidth, reqheight)` coordinates that overflow screen bounds.
4. Version & Release Lock:
   - Keep `__init__.__version__ == "1.4.15"` UNCHANGED.
   - `v1.5.0` remains CANCELLED / NOT RELEASED / VERSION PROMOTION NOT AUTHORIZED.
   - NEVER run `git add`, `git commit`, `git push`, `git reset`, or `git clean`.

==================================================
PART 1 — PREFLIGHT & READ-ONLY SOURCE/RUNTIME AUDIT
==================================================
1. Preflight Verification (report verbatim):
   - `git -C D:\Misora-Editor rev-parse --show-toplevel`
   - `git -C D:\Misora-Editor branch --show-current`
   - `git -C D:\Misora-Editor rev-parse HEAD` (capture exact post-DOCS-01 HEAD `<POST_DOCS01_HEAD>`)
   - `git -C D:\Misora-Editor status --short --untracked-files=all` (MUST be empty)
   - `py -3.12 -B -c "import __init__; print(__init__.__version__)"` (MUST be `1.4.15`)
   - `py -3.12 -B tools/generate_symbol_index.py --check` (MUST exit 0)
   - `py -3.12 -B -c "import unittest; s=unittest.TestLoader().discover('tests'); print('countTestCases:', s.countTestCases())"` (expected exact `494`)
   - Record exact `misora.py` logical line count and pure CRLF count (backslash-free Python using `bytes([13,10])`, `bytes([10])`, `bytes([13])`).
2. Targeted Source Audit & Runtime Reproduction:
   - Quote the complete `ToolTip` class and `create_tooltip` function verbatim with exact line numbers.
   - Verify whether `show_tip()` sets `wm_geometry()` BEFORE measuring `winfo_reqwidth()` / `winfo_reqheight()`, and whether it clamps against screen / monitor work-area bounds on X and Y axes.
   - Check how Windows multi-monitor virtual screen / monitor work area (`GetMonitorInfoW` / `MonitorFromPoint` via stdlib `ctypes` on Windows with safe Tk `vrootx/vrooty/vrootwidth/vrootheight` or `screenwidth/screenheight` fallback) can be queried cleanly WITHOUT changing DPI awareness (AGENTS.md Rule 23) and with full deterministic testability (e.g., injectable/pure helper function `_compute_tooltip_geometry(...)` or `_get_monitor_work_area(widget, x, y)`).

==================================================
PART 2 — REQUIRED PLAN SECTIONS (`T-08a_Implementation_Plan.md`)
==================================================
Include ALL of the following (applying every review standard locked across T-01, T-02, and DOCS-01):
1. Preflight transcript at exact `<POST_DOCS01_HEAD>` (`countTestCases: 494`, clean tree, `--check` PASS, version `1.4.15`, line count & pure CRLF check).
2. Verbatim `ToolTip` source audit + read-only runtime probe output proving the exact un-clamped coordinates overflowing right/bottom bounds on a genuine `MisoraApp`.
3. Minimal, clean root-cause fix design in `misora.py`:
   - Extract/implement a clean, pure-geometry positioning helper (e.g., `_compute_tooltip_position(widget_x, widget_y, widget_w, widget_h, tip_w, tip_h, work_left, work_top, work_right, work_bottom)` or equivalent clean design inside `ToolTip`) AND safe monitor work-area query (handling Windows multi-monitor including negative coordinates & taskbar work area, with Tk fallback on non-Windows/errors; ZERO changes to DPI awareness).
   - Measure actual tooltip dimensions (`tw.update_idletasks()`, `winfo_reqwidth()`, `winfo_reqheight()`) BEFORE applying final `wm_geometry(f"+{x}+{y}")` (preventing flicker via `withdraw()` -> measure -> `wm_geometry` -> `deiconify()` or equivalent clean Tk sequence).
   - Positioning rules:
     * Default: near trigger widget (`x = widget_x + 8`, `y = widget_y + widget_h + 4`, or exact existing offset).
     * Right overflow (`x + tip_w > work_right - margin`): clamp/shift left into `[work_left + margin, work_right - tip_w - margin]`.
     * Left overflow (`x < work_left + margin`): clamp to `work_left + margin`.
     * Bottom overflow (`y + tip_h > work_bottom - margin`): flip ABOVE trigger widget (`widget_y - tip_h - 4`), then clamp into `[work_top + margin, work_bottom - tip_h - margin]`.
     * Top overflow (`y < work_top + margin`): clamp to `work_top + margin`.
     * Multi-monitor negative coordinates (e.g. secondary monitor at `[-1920, 0)`) MUST work identically without ever clamping negative valid coordinates to `0`!
   - Preserve `setattr(self.widget, "_tooltip", self)`, 350ms delay timer, tooltip text/wrapping, and `hide_tip()` behavior untouched.
   - Provide exact unified diff, verbatim context lock (`V-1`, `git apply --check`), exact post-edit line count (`V-2`), pure CRLF + `bare_CR == 0` check (`C-5`), and exact `git diff --numstat -- misora.py`.
4. Strict File Ownership Matrix under a dedicated Project Lead-approved T-08a Execution Charter:
   - Allowed ONLY after explicit `Proceed`:
     * `misora.py` (minimal `ToolTip` positioning & work-area helper fix ONLY)
     * `tests/test_t08a_tooltip_clamping.py` (NEW — stdlib `unittest`, zero `pytest`, zero `.unity3d`, zero `skipTest()`, patching `CONFIG_PATH` & `messagebox` to temp dir, clean `app.destroy()` + `shutil.rmtree` in `tearDown`)
     * `docs/project/OPEN_ISSUES.md` (T-08a row ONLY: automated TDD `PASS`, Windows QA `M-1..M-6` `MANUAL-PENDING`, Lifecycle stays `ACTIVE`, N-4 transient `--check` note)
     * `PROJECT_STATE.md` (exact `494 + N = (451 + N) PASS + 35 SKIP + 6 FAIL + 2 ERROR`, N-4 transient `--check` note, stay `<= 15,360` bytes)
   - Strictly FORBIDDEN / READ-ONLY: `__init__.py`, `core/**`, `assets/**`, all existing `tests/*.py`, `AGENTS.md`, `docs/archive/**`, `tools/generate_symbol_index.py`, `docs/architecture/MISORA_SYMBOL_INDEX.md` (deferred to Project Lead post-commit regeneration), `misora.bat`, `requirements.txt`, `misora_config.json`, `backups/**`, `README.md`.
5. Strict Zero-`.pyc` Windows-Safe TDD Verification Plan:
   - Defect Probes (MUST FAIL pre-patch with `0 errors`, PASS post-patch):
     * Right-edge overflow on genuine `MisoraApp` / `ToolTip` (e.g., widget near right edge of `1920x1080` monitor with long 2-line T-02 tooltip -> clamped inside right bound)
     * Bottom-edge overflow (flips above widget / clamped inside bottom bound)
     * Left-edge & Top-edge clamping
     * Multi-monitor negative-coordinate work area (e.g., `[-1920, 0, 0, 1040]` -> tooltip stays inside secondary monitor, never jumps to `0`)
   - Regression Guards (MUST PASS pre- and post-patch; include N-3 Guard Re-Label Rule):
     * Center-screen tooltip keeps standard near-widget position
     * `widget._tooltip.text` and 2-line T-02 tooltip text preserved verbatim
     * `hide_tip()` cleanly destroys Toplevel without TclError
   - Broad BOM-safe (`bytes([239,187,191])`) in-memory `compile()` across `__init__.py`, `misora.py`, `core/*.py`, `assets/*.py`, `tests/*.py` (NO `compileall`), plus `pre_pyc_count == post_pyc_count`.
   - Exact discovery math `494 + N`; pre-patch exact `FAILED (failures=P)` with **0 errors**; post-patch T-08a suite `N/N OK` -> targeted UI suites (`test_t02_next_tooltip`, `test_v15_s11e_polish_splash_menu_tooltips`) -> full `py -3.12 -B -m unittest discover -s tests -v` asserting exact `(494 + N) = (451 + N) PASS + 35 SKIP + 6 FAIL + 2 ERROR`.
6. Complete 4-File Rollback Steps pinned to exact `<POST_DOCS01_HEAD>` (NO `reset --hard`, restoring `misora.py`, `docs/project/OPEN_ISSUES.md`, `PROJECT_STATE.md`, removing `tests/test_t08a_tooltip_clamping.py`, re-verifying clean tree, `494` tests, and original `misora.py` line count).
7. Manual Windows QA Checklist (`M-1..M-6` covering `lbl_char_overflow` right edge at 100% & 125% DPI maximized, bottom-bar tooltip e.g. Save/Revert flipping upward, left/top widgets, multi-monitor if available, and operator sign-off) marked `MANUAL-PENDING`.

Verify `git status --short --untracked-files=all` in `D:\Misora-Editor` is still 100% clean, report the written path + SHA-256 of `T-08a_Implementation_Plan.md`, and end with:
`STOP — WAITING FOR INDEPENDENT REVIEW`.

```

Cek dulu status commit `DOCS-01` dengan 4 perintah di §1; begitu `DOCS-01` sudah bersih ter-commit & ter-push, langsung jalankan prompt **`T-08a`** di atas di Antigravity lalu unggah `T-08a_Implementation_Plan.md` ke sini!