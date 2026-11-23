# Technical Architecture & File Formats

## 1. Database Taxonomy Engine (`modules/db_explorer.py`)

`PriconneDBExplorer` opens `master.db` strictly in SQLite **read-only URI mode** (`?mode=ro`) to prevent accidental corruption. On startup it inspects `sqlite_master` and `PRAGMA table_info()` to discover:
- Every non-empty table containing at least one `TEXT`/`CHAR`/`CLOB` column.
- Exact primary key columns (including composite keys), falling back to SQLite `rowid` when a table has no explicit primary key.
- Automatic folder classification via ordered regex rules in `CATEGORY_RULES`, with an automatic `99_uncategorized_text` fallback so newly added tables in future JP patches are never missed.

## 2. Japanese CDN Content-Addressed Pool (`modules/cdn_bridge.py`)

Cygames serves Japanese game assets via Akamai under MD5-prefixed buckets:

```text
https://prd-priconne-redive.akamaized.net/dl/pool/<PoolName>/<md5[0:2]>/<md5>
```

| Asset Type | Pool Name |
| :--- | :--- |
| Unity AssetBundles (`a/*.unity3d`) | `AssetBundles` |
| Audio (`v/`, `b/`, `s/` `.acb`/`.awb`) | `Sound` |
| Video (`m/*.usm`) | `Movie` |

Every downloaded file is verified against its manifest MD5 digest before being saved to `input/`.

## 3. Lossless ADV Story Binary Format (`modules/story_codec.py`)

Inside `a/storydata_storydata_<7-digit-id>.unity3d`, the story script is stored as a Unity `TextAsset` whose payload consists of sequential binary records:

```text
Record:
  uint16_be  command_id
  Repeat:
    uint32_be  arg_length       (0 terminates the record)
    bytes      encoded_arg      (present only when arg_length > 0)
```

Each `encoded_arg` is decoded by:
1. Bitwise-inverting (`~b & 0xFF`) every 3rd byte starting at index `0` (`0, 3, 6, ...`).
2. Base64-decoding the resulting buffer.
3. Decoding as UTF-8 (`surrogateescape` preserves any non-standard bytes losslessly).

During repacking, unchanged arguments reuse their exact original byte slices, guaranteeing **byte-exact round-trips** verified by re-reading the written `.unity3d` bundle from disk.
