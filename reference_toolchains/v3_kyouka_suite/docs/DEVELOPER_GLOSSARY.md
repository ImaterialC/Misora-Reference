# Cygames Developer Codename Glossary

*Princess Connect! Re:Dive* uses internal developer codenames across both `master.db` tables and Japanese CDN AssetBundle paths. Use this reference sheet to decode what any file or table actually contains.

---

## 1. Where Game Text Actually Lives

| Text Type | Primary Location | Key Tables / Asset Patterns |
| :--- | :--- | :--- |
| **Main / Event / Bond Story Titles** | `master.db` | `story_data`, `story_detail`, `event_story_detail`, `hatsune_description` |
| **Main / Event / Bond Dialogue Scripts** | **JP CDN AssetBundle** | `a/storydata_storydata_<7-digit-id>.unity3d` |
| **Cutscene Anime Subtitles** | **JP CDN AssetBundle** | `a/movie_subtitle_*.unity3d` (MonoBehaviour `recordList`) |
| **Tutorial & Tips** | `master.db` + **CDN** | `tutorial_*`, `tips`, `help_detail`, plus `0000xxx` story bundles |
| **Home Screen Dialogue** | `master.db` | `unit_comments`, `my_page_*`, `unit_mypage_*`, `birthday_*` |
| **Guildhouse Chirping** | `master.db` | `room_unit_comments`, `room_chat_info`, `room_chat_scenario`, `room_item` |
| **Unit Profiles & Bios** | `master.db` | `unit_data`, `unit_profile`, `unit_introduction`, `guild`, `album_*` |
| **Unit Skills & Ailments** | `master.db` | `skill_data`, `skill_action`, `sp_skill_*`, `ailment_data` |
| **Glossary & Lore** | `master.db` | `glossary_detail`, `help_category`, `help_detail` |
| **Monster Names & Bestiary** | `master.db` | `enemy_parameter` (wave display names), `unit_enemy_data` (monster lore) |
| **UI, Missions & System Pop-ups** | `master.db` + **UI Prefabs** | `system_message`, `er_message`, `mission_*`, `quest_*`, `item_data`, `equipment_data` |

---

## 2. Japanese CDN Top-Level Path Prefixes

| Prefix | Asset Format | Purpose | Translatable? |
| :--- | :--- | :--- | :--- |
| **`a/`** | `.unity3d` | Unity AssetBundles (story scripts, subtitles, UI prefabs, textures) | **Yes (Primary)** |
| **`m/`** | `.usm` | Criware anime movies & Union Burst cutscenes | Subtitles are in `a/` |
| **`v/`** | `.acb` / `.awb` | Character voice acting & story dialogue audio | Context reference |
| **`b/`** | `.acb` / `.awb` | Background music (BGM) | No |
| **`s/`** | `.acb` / `.awb` | Sound effects (SE) | No |

---

## 3. Internal Feature & Table Codenames

| Developer Code | Real In-Game Feature | Origin / Translator Notes |
| :--- | :--- | :--- |
| **`hatsune`** | **Monthly Story Events** | Named after JP's very first event (*"Hatsune's Present"*, 2018). Used permanently for ALL story events. |
| **`shiori`** | **Side Stories** | Wordplay on Japanese *shiori* (bookmark) and character Shiori. Permanent archive of past events. |
| **`storydata`** | **ADV Visual Novel Script** | Binary script with every 3rd byte inverted + Base64. Extracted via `Kyouka-Asset-Explorer.py`. |
| **`adv`** | **Adventure / Story Scene** | Backgrounds (`bg_adv`), voices (`vo_adv`), and scene assets. |
| **`room`** | **Guildhouse** | Chibi idle lines (`room_unit_comments`), multi-character skits (`room_chat_scenario`), and furniture (`room_item`). |
| **`mypage`** | **Home Screen** | Home screen unit comments, banners, and dynamic layouts. |
| **`still`** | **Story / Bond CG** | Full-screen illustrations shown during scenes. |
| **`telop`** | **Title Card Overlay** | Episode title text shown over screen transitions (`title_telop`). |
| **`emblem`** | **Player Titles** | Unlockable profile badges/titles (`称号`). |
| **`dear`** | **Trust / Affection Mode** | Special trust-building sub-stories (collabs & special events). |
| **`tower`** | **Luna Tower** | Tower floors and crossover character stories (`tower_story_*`). |
| **`clan_battle`** | **Clan Battle** | Monthly raid boss names, mechanics, and lore. |
| **`tdf`** | **Dimension Fault** | Multi-phase endgame exploration mode. |
| **`abyss`** | **Abyssal / Deep Zone** | High-difficulty elemental quests. |
| **`talent`** | **Elemental Attributes** | Fire, Water, Wind, Light, Dark elements & Princess Knight system. |
| **`er_message`** | **Error Messages** | Network, maintenance, and system validation pop-ups. |
| **`spine`** | **Spine2D Chibi Rig** | 2D skeletal animations (no text). |
| **`prefab`** | **Unity UI Layout** | Static UI buttons and settings screens not loaded from `master.db`. |

---

## 4. Numeric ID Decoding Cheat Sheet

### Unit IDs (6 digits)
- **`1xxxxx`** — Playable character (`105801` = Pecorine 1★, `105831` = 3★, `105861` = 6★). First 4 digits identify the base character.
- **`3xxxxx`** — Monster / Enemy / Raid Boss.
- **`5xxxxx`** — Story-only NPC or guest unit.

### Story IDs (7 digits in `storydata_<id>`)
- **`0000xxx`** — Prologue & opening tutorial.
- **`1xxxxxx`** — Character Bond Story (`1058001` = Pecorine Bond Episode 1).
- **`2xxxxxx`** — Main Story.
- **`3xxxxxx`** — Guild Story.
- **`4xxxxxx`** — Extra / Birthday / Special Story.
- **`5xxxxxx`** — Event Story (`hatsune`) & Side Story (`shiori`).
