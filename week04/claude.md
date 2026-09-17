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
  dimmed styling via the `.todo-item.completed` CSS class (completed
  items are NOT re-sorted to the bottom — dimming was the chosen
  approach when given a choice between the two).
- Category filter tabs (전체/업무/개인/공부) that show/hide list items.
- Progress bar + label (`"7 / 15 완료 (47%)"`), recalculated on every
  render; shows "등록된 할 일이 없습니다" instead when the list is empty.
- `loadTodos()` fails safe to `[]` (empty list, no thrown error) when
  `localStorage` has no entry, invalid JSON, or valid JSON that isn't an
  array — covered by a headless jsdom regression test (add/edit/delete/
  toggle/filter/progress + persistence across a simulated reload, plus
  the three malformed-storage cases above), all passing.

## Notes
- All code and comments are written in English; user-facing UI text is
  Korean (업무/개인/공부 category labels etc.), matching the target user.
- The todo data shape is `{ id, title, category, completed, createdAt }`
  — note the field is `title`, not `text`.
- Category values are stored internally as `work`/`personal`/`study`
  and mapped to Korean labels via `CATEGORY_LABELS` — keep that mapping
  as the single source of truth if labels change.
