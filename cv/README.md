# Updating the CV

Everything on `cv.html` comes from the files in this folder. You never edit `cv.html` itself.

**After any change, run:**

```bash
python generate-data.py
```

Then commit and push as usual.

## Where things live

| On the page | File |
|---|---|
| Name, title, summary, links | `profile.md` |
| Overview → Selected work (4 cards) | `featured.md` |
| Overview → Focus areas | `focus.md` |
| Experience tab | `experience/*.md` — one file per role |
| Projects tab | `projects.md` |
| Public work tab | `public-work/*.md` — one file per item |
| Education tab | `education.md` |
| Photos | `images/` |

## Adding a talk, PR, video or post

1. Copy `public-work/_TEMPLATE.md` and rename it, e.g. `2026-10-pydata-talk.md`.
2. Fill in the lines at the top. Set `draft: false` when it's ready.
3. Run `python generate-data.py`.

## Adding a role

Copy one file in `experience/`. Older roles get `earlier: true` and show as a single line.

## Placeholders and preview

Anything in square brackets like `[outcome]` is a reminder to fill in.

- On the live site, placeholders and `draft: true` items are **hidden**.
- Open `cv.html?preview` to see them highlighted in yellow.

## PDF

The "Download PDF" button opens the browser's print dialog with a clean, all-sections layout. Choose "Save as PDF".
