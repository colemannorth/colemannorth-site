# colemannorth.com

Minimal photo portfolio. Static site hosted free on Cloudflare Pages.

- `index.html` – photo grid (reads `photos.json`), click for full-screen viewer
- `about.html` – bio; add your headshot at `photos/about/portrait.jpg`
- `build_photos.py <folder>` – turns a folder of originals into web images + `photos.json`
  (resizes, fixes rotation, strips GPS/metadata, removes deleted photos, newest first)

Updating photos: drop photos in the Google Drive folder → the nightly scheduled task
runs the build script and pushes to GitHub → Cloudflare republishes automatically.
