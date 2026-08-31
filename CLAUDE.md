# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Flask expense-tracker app used as a **step-by-step learning project**. The frontend (landing page, auth pages, base layout, CSS) is fully built; the backend is a scaffold with explicit "students will implement this" placeholders. Routes like `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete` in `app.py` currently just return a plain string like `"Add expense — coming in Step 7"` — these are intentionally unimplemented, not bugs. When asked to build out a feature, implement it in place of the placeholder rather than treating the stub as broken code to preserve.

`database/db.py` is an empty scaffold with a comment specifying the contract to implement:
- `get_db()` — SQLite connection with `row_factory` and foreign keys enabled
- `init_db()` — creates tables using `CREATE TABLE IF NOT EXISTS`
- `seed_db()` — inserts sample dev data

## Running the app

```bash
# Windows venv is already set up at ./venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py   # serves on http://127.0.0.1:5001 (debug=True)
```

Tests use `pytest` + `pytest-flask` (both in `requirements.txt`), though no test files exist yet — add them under a `tests/` directory as backend functionality is implemented.

## Repository quirks

- There is a duplicate nested `expense-tracker/` directory and a `__MACOSX/` directory at the repo root — leftovers from unzipping the original archive. Both are git-ignored and should be ignored/not edited; the real project root is the top-level directory containing this file.
- `expense_tracker.db` (SQLite file) and `venv/` are git-ignored — don't commit them.

## Architecture

- **`app.py`** — single-file Flask app; all routes defined directly on `app`, no blueprints. Templates are rendered with `render_template`, no view models yet.
- **`templates/base.html`** — shared layout (nav, footer, Google Fonts, `static/css/style.css`, `static/js/main.js`) that every page extends via `{% block content %}`. Nav/footer links use `url_for('landing')`, `url_for('login')`, `url_for('register')`, `url_for('terms')`, `url_for('privacy')` — add new routes the same way rather than hardcoding paths.
- **`static/css/style.css`** — single global stylesheet (~750 lines) covering the landing page, auth forms, and footer/nav. No CSS framework; follow existing class-naming patterns (e.g. `auth-section`, `auth-card`, `form-group`, `btn-submit`) when adding markup.
- **`static/js/main.js`** — currently empty; this is where client-side behavior (e.g. the landing page's YouTube modal) is added.
- **`database/db.py`** — intended as the single place for SQLite access; not yet implemented (see above). When implementing, wire `init_db()`/`seed_db()` to be called from `app.py` on startup rather than adding ad-hoc connection logic in routes.
