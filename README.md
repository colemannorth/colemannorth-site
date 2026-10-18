# colemannorth.com

Minimal photo portfolio. Static site hosted free on Cloudflare Pages.

- `index.html` – photo grid (reads `photos.json`), click for full-screen viewer
- `about.html` – bio; add your headshot at `photos/about/portrait.jpg`
- `build_photos.py <folder>` – turns a folder of originals into web images + `photos.json`
  (resizes, fixes rotation, strips GPS/metadata, removes deleted photos, newest first)

Updating photos: add/remove photos in the Google Drive "Portfolio" folder. Every night
`.github/workflows/sync-photos.yml` downloads it, runs the build script and commits →
Cloudflare republishes automatically. To update right away: Actions tab → "Sync photos
from Google Drive" → Run workflow.
