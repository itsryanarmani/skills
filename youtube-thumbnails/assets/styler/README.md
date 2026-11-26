# Thumbnail styler

One HTML page to pick a thumbnail style for many videos. It shows 11 presets, each
copied from a real thumbnail (its colours, font, size and tilt were measured), with
the real thumbnail beside ours. Below the presets are controls for background,
font, outline, placement and logo. A layout button picks the pose.

```
styler/
  styler.html
  config.json    same shape as ../gallery/config.example.json: a name and one item per video
  cuts/<pose>.png    transparent cutouts of the person (make them with thumbnail-cutout)
  poses/<pose>.png   the full pose photos, used by the "photo" background
  logos/white.svg  logos/black.svg    your logo in two colours
  refs/<id>.jpg      real thumbnails for the side-by-side (optional)
```

Serve the folder and open the page:

```bash
python3 -m http.server 8766 --directory styler
```

- Pick a preset, a layout and a few controls. The Copy button gives the settings as
  JSON.
- `#solo=1&i=N&s=<json>` renders one 1280x720 thumbnail for item N and sets
  `<html data-ready>` to `ok`, or to `fail:<reason>` (`image missing`, `unknown item`,
  `bad style`, `text too small`, `config`, `render`). Open it in a headless browser
  at 1280x720, wait for `ok`, and save a screenshot. It does not use the
  `thumbnail-export` hash (`l=LAYOUT`), which belongs to `../gallery/index.html`. Then
  use `youtube-thumbnail-set` to put the files on the videos.
- The presets name real videos by id in `refs/`. Download those thumbnails with
  `thumbnail-dataset` if you want the side-by-side. They are other people's work:
  keep them local and never commit them.
- Layout names in the page (shocked, thinking, headhands, shush, shrug, mindblown)
  match the pose file names, so the `cuts/` and `poses/` files must use those names.
- Fonts load from Google Fonts, so the first load needs the network. Offline, a fallback
  font is used and the page still says `ok`: check the text by eye.
