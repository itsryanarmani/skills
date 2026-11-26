# Thumbnail gallery

One HTML page that shows 34 thumbnail layouts for each item, at 1280x720, with a
pose picker, a 240 px and 120 px phone-size test, and a safe-zone view for the
bottom-right duration badge. Layouts are written in `index.html` (`LAYOUTS`
use a pose, `CUT` use a transparent cutout).

## Folder

```text
gallery/
  index.html          this file
  config.json         copy of config.example.json with your items
  poses/index.json    ["pointing","sad",...]  the tags you have
  poses/<tag>.png     a person on one flat colour, left half empty
  cutout.png          optional: transparent PNG of the person (adds 10 layouts)
```

`name` is used by the "Breaking news" layout. `quote` is used by "Quote"; `{C}`
is the item title. `sub` is a short second line (a role, a topic).

## Run

```bash
thumbnail-poses --ref photo.jpg --out gallery/poses --yes   # makes poses and index.json
python3 -m http.server 8765 --directory gallery             # then open http://127.0.0.1:8765/
thumbnail-export --gallery gallery --out thumbs --layout 5 --item all
```

Serve the folder over HTTP. A page opened from `file://` cannot read the pose
pixels it uses to pick a text colour. In the page, click a layout to preview it,
click a pose to apply it to every layout, and press the button to note a choice.

## Add a layout

Add a row to `LAYOUTS`: `[name, default pose tag, (title, sub, style) => html]`.
`style` has `bg`, `ink` (text colour) and `hi` (accent), read from the pose.
Use `T(...)` for a text block and `PILL(...)` for a label. Text blocks size all
their lines alike. Keep text to four words and out of the bottom-right corner.
