<!-- Created: 2026-09-17 11:10:26 -->
# week04 — To-Do App

## Purpose
A personal to-do list for managing roughly 10-20 tasks a day: add/edit/
delete, mark complete, categorize as work/personal/study, and see
overall progress. See `PRD.md` for the full requirements.

## Tech stack
- Plain HTML/CSS/JavaScript only — no framework, no build step, no
  dependencies.
- Data is persisted to the browser's `localStorage` (key
  `week04_todos`), so it survives page reloads. There is no backend.

## Files
- `PRD.md` — product requirements.
- `index.html` — page structure (add form, category filter, todo list,
  progress bar).
- `style.css` — styling.
- `app.js` — all app logic: state, localStorage persistence, rendering,
  and event handling.
- `Open_App.bat` — double-clickable launcher (Windows Explorer): opens
  `index.html` directly in the default browser.

## How to run
Just open `index.html` in a browser (double-click it, or double-click
`Open_App.bat`). No server or install step needed.

## Notes
- All code and comments are written in English; user-facing UI text is
  Korean (업무/개인/공부 category labels etc.), matching the target user.
- Category values are stored internally as `work`/`personal`/`study`
  and mapped to Korean labels via `CATEGORY_LABELS` in `app.js` — keep
  that mapping as the single source of truth if labels change.
