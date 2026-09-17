<!-- Created: 2026-09-17 11:10:26 -->
# week04 — To-Do App

## Purpose
A personal to-do list for managing roughly 10-20 tasks a day: add/edit/
delete, mark complete, categorize as work/personal/study, and see
overall progress. See `PRD.md` for the full requirements.

## Tech stack
- A single `index.html` file — HTML, CSS (in a `<style>` block), and
  JavaScript (in a `<script>` block) all in one place. No framework, no
  build step, no dependencies, no other files to load.
- State (a plain `todos` array) is persisted to `localStorage` (key
  `week04_todos`) on every add/edit/delete/completion-toggle, and
  reloaded on page load — see `loadTodos()`/`saveTodos()`.

## Files
- `PRD.md` — product requirements.
- `index.html` — the entire app: layout, styling, and logic.
- `Open_App.bat` — double-clickable launcher (Windows Explorer): opens
  `index.html` directly in the default browser.

## How to run
Just open `index.html` in a browser (double-click it, or double-click
`Open_App.bat`). No server or install step needed.

## Implemented (feature-complete per PRD.md)
- Add / inline edit / delete todos, persisted to `localStorage`.
- Completion checkbox: toggles `completed`, applies strikethrough +
  dimmed styling via the `.todo-item.completed` CSS class, AND sorts
  completed items to the bottom of the (filtered) list on render —
  sorting is done on a copy in `render()`, it doesn't mutate/reorder the
  underlying `todos` array or its saved order.
- Category filter tabs (전체/업무/개인/공부) that show/hide list items.
- Progress bar + label (`"7 / 15 완료 (47%)"`), recalculated on every
  render; shows "등록된 할 일이 없습니다" instead when the list is empty.
- On a genuinely fresh start (no `localStorage` entry yet), `loadTodos()`
  returns 3 built-in `SAMPLE_TODOS` instead of an empty list, so the app
  isn't blank the first time it's opened. Invalid JSON or valid JSON
  that isn't an array still fails safe to a real empty list (`[]`), not
  samples — that's treated as an error case, not a fresh install.
- Covered by a headless jsdom regression test (add/edit/delete/toggle/
  filter/progress + persistence across a simulated reload, plus the
  sample-data and malformed-storage cases above), all passing.

## Notes
- All code and comments are written in English; user-facing UI text is
  Korean (업무/개인/공부 category labels etc.), matching the target user.
- The todo data shape is `{ id, title, category, completed, createdAt }`
  — note the field is `title`, not `text`.
- Category values are stored internally as `work`/`personal`/`study`
  and mapped to Korean labels via `CATEGORY_LABELS` — keep that mapping
  as the single source of truth if labels change.
