# Complete User Tutorial (English)

This guide walks you through setting up **Kyouka Asset Explorer**, locating any text you see inside *Princess Connect! Re:Dive*, translating it, and repacking or patching your translations.

---

## Step 1: Installation & Setup

1. Install **Python 3.10 – 3.14** (ensure *"Add Python to PATH"* is checked on Windows).
2. Download the latest decrypted Japanese `master.db` (for example from `https://roboninon.win/db/download`) and place it inside the `Kyouka-Asset-Explorer/` folder:
   ```text
   Kyouka-Asset-Explorer/
   ├── Kyouka-Asset-Explorer.bat
   ├── Kyouka-Asset-Explorer.py
   ├── master.db
   └── modules/
   ```
3. *(Optional, for `.unity3d` story extraction/repacking)* Open a terminal inside the folder and run:
   ```bash
   pip install -r requirements.txt
   ```
4. Launch the tool by double-clicking **`Kyouka-Asset-Explorer.bat`** (Windows) or running `python Kyouka-Asset-Explorer.py`.

---

## Step 2: Reverse-Lookup Any Text Seen In-Game (`master.db`)

Whenever you see a Japanese string in the game (a monster name, skill description, Guildhouse chirp, or error message) and do not know where it is stored:

1. Select **Option 1 (`Global Full-Text Search`)**.
2. Paste or type the exact text (e.g., `コボルト`, `Lizardman`, or a Guildhouse sentence).
3. The explorer scans **every text column of every table** and displays a summary showing:
   - Exact SQLite **Table Name**
   - Assigned **Category Folder**
   - Number of hits and a sample match
4. Choose your next action right from the search results:
   - `v 1` — View detailed matches (Primary Key, column name, and full text) for result #1.
   - `e 1` — Export **only** table #1 as `.csv` and `.translation.json`.
   - `f 1` — Export the **entire related category folder** (for instance, finding one monster in `enemy_parameter` lets you export ALL enemy/monster tables into `exports/07_monsters_and_enemies/` in one command).

---

## Step 3: Translating Exported Files

Open the `exports/` folder. Each exported table produces two synchronized formats:

1. **`<table_name>.csv`**
   - Saved in **UTF-8 with BOM**, so Japanese characters render cleanly in Microsoft Excel and Google Sheets.
   - Next to every text column (`name`, `description`, etc.), an empty `<column>_translation` column is automatically provided.
2. **`<table_name>.translation.json`**
   - Ideal for CAT tools (Crowdin, Weblate, ParaTranz) and automated DB patching:
     ```json
     {
       "key": "enemy_parameter:enemy_id=101010101:name",
       "table": "enemy_parameter",
       "pk": "enemy_id=101010101",
       "column": "name",
       "source": "コボルト",
       "translation": "Kobold"
     }
     ```
   - Fill in the `"translation"` field. Leave untouched entries blank (`""`) so the re-injector preserves the original text.

### Building a Patched Database
Once you finish translating any `.translation.json` files inside `exports/`, run **Option 5 (`Re-Inject Translations`)** or:
```bash
python Kyouka-Asset-Explorer.py reinject-db
```
This creates a safe patched copy at **`output/master_patched.db`** without modifying your original `master.db`.

---

## Step 4: Extracting & Translating Main / Event / Bond Stories

> **Important:** Dialogue scripts for Main Story, Event Story, Character Bond Story, and Guild Story are **NOT stored inside `master.db`**. `master.db` only stores their Story IDs and episode titles.

### Method A: Download Directly from the Japanese CDN
1. Place your JP manifest CSV file(s) inside the `manifests/` folder (see `manifests/README.md`).
2. Select **Option 7 (`JP CDN Asset Bridge`)** -> **Sub-option 1 (`Search Story in master.db`)**.
3. Search by Story ID or title. The tool automatically:
   - Maps the `story_id` to `a/storydata_storydata_<id>.unity3d`
   - Decodes the asset name using the Developer Glossary
   - Checks your BepInEx `RedirectedResources` folder (if `--bepinex` was provided)
   - Downloads the bundle from `prd-priconne-redive.akamaized.net` and verifies its MD5 hash
   - Auto-extracts the script into `text/*.txt` (requires `UnityPy`)

### Method B: Extract Local `.unity3d` Bundles
1. Copy any `.unity3d` story or movie subtitle bundles into the `input/` folder.
2. Run **Option 8 (`Extract Local .unity3d`)** -> scripts appear in `text/` as lossless v2.1 `.txt` (stories) or `.json` (subtitles).
3. Translate the dialogue lines inside `text/*.txt` (keep command names, `System`/`Motion`/`Effect` lines, and escape sequences like `\n` intact).
4. Run **Option 9 (`Repack Local .unity3d`)** -> verified patched bundles are written to `output/`, ready for BepInEx `RedirectedResources`.

---

## Step 5: Publishing Your Project on GitHub

This repository already includes a pre-configured **`.gitignore`** that automatically blocks `master.db`, `.unity3d` bundles, `exports/`, `input/`, `text/`, and `output/` from being accidentally committed.

```bash
git init
git add .
git commit -m "Initial commit: Kyouka Asset Explorer"
git branch -M main
git remote add origin https://github.com/<your-username>/Kyouka-Asset-Explorer.git
git push -u origin main
```
