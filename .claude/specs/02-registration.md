# Spec: Registration

## Overview
This step implements user account creation for Spendly. The landing page and the `register.html` template already exist with a POST form to `/register`, but the `/register` route only handles GET and does not persist users. This step wires the form to `database/db.py`'s `users` table so a visitor can create an account, have their password hashed and stored, and be redirected into the app (session-based login of the new user). This is the second step of the roadmap, following database setup, and is a prerequisite for login/logout (Step 3) and any authenticated route (profile, expenses).

## Depends on
- Step 1 — Database setup (`database/db.py` schema: `users` table with `id`, `name`, `email`, `password_hash`, `created_at`).

## Routes
- `GET /register` — renders the registration form — public (already exists, no change to method needed)
- `POST /register` — validates input, checks email uniqueness, hashes password, inserts user, starts a session, redirects to the profile/dashboard — public

## Database changes
No database changes. The existing `users` table in `database/db.py` (`id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, created_at TEXT DEFAULT (datetime('now'))`) already supports registration as-is.

## Templates
- **Create:** none
- **Modify:** `templates/register.html` — add server-rendered field-level/general error handling for: missing fields, invalid email format, password too short (<8 chars, matching the placeholder text "Min. 8 characters"), and duplicate email. Repopulate `name` and `email` values on validation failure so the user doesn't retype them. No structural/CSS changes needed — reuse the existing `auth-error` block already present.

## Files to change
- `app.py` — implement `POST` handling on the `/register` route: read form data, validate, hash password with werkzeug, insert into `users` via `get_db()`, set session, redirect.
- `templates/register.html` — repopulate submitted values on error; ensure error rendering covers new validation messages.

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security` (already a Flask dependency, already imported in `database/db.py`) provides `generate_password_hash`. Flask's built-in `session` covers login state.

## Rules for implementation
- No SQLAlchemy or ORMs — use `sqlite3` via `database.db.get_db()` only.
- Parameterised queries only — never interpolate/format user input into SQL strings.
- Passwords hashed with werkzeug (`generate_password_hash` / `check_password_hash`), never stored or logged in plaintext.
- Use CSS variables — never hardcode hex values in any CSS/inline styles touched.
- All templates extend `base.html`.
- Use a Flask `secret_key` (from `app.config` or an env var) before using `session` — do not skip this or sessions will silently fail.
- Validate email format and password length server-side even though the HTML form has `required`/`type=email` — client-side validation is not trustworthy.
- On duplicate email, show a friendly error (e.g. "An account with this email already exists.") rather than a raw SQLite `IntegrityError`.

## Definition of done
- [ ] Visiting `/register` shows the existing registration form unchanged in layout.
- [ ] Submitting valid name/email/password creates a new row in `users` with a hashed (not plaintext) password.
- [ ] After successful registration, the user is redirected away from `/register` (e.g. to `/profile`) and is in a logged-in session.
- [ ] Submitting an email that already exists in `users` re-renders the form with an error and does not create a duplicate row.
- [ ] Submitting a password under 8 characters re-renders the form with an error and does not create a user.
- [ ] Submitting with a missing field (name, email, or password) re-renders the form with an error and does not create a user.
- [ ] Previously entered name/email are preserved in the form fields after a validation error.
- [ ] No plaintext password ever appears in the database, logs, or a redirect/query string.
