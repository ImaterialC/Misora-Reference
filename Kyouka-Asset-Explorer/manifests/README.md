# Manifests Folder

Place your Japanese server manifest CSV files here (for example: `storydata_assetmanifest`, `movie_assetmanifest`, or `manifest_assetmanifest`).

Each manifest line follows Cygames' standard comma-separated format:

```csv
a/storydata_storydata_1058001.unity3d,0123456789abcdef0123456789abcdef,0,12345,storydata
```

When `Kyouka-Asset-Explorer.py` starts, it automatically indexes every valid manifest file placed inside this folder so you can search and download bundles directly from the official Japanese CDN (`prd-priconne-redive.akamaized.net`).
