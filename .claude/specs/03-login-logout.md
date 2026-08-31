# Spec: Login and Logout

## Overview
This step implements session-based authentication for returning users. The `login.html` template already exists with a POST form to `/login`, but the `/login` route only handles GET, and `/logout` is a placeholder that returns plain text. This step wires `/login` to verify credentials against the `users` table (created in Step 1, populated by Step 2's registration) and start a session, and wires `/logout` to clear that session. This is the third step of the roadmap, following database setup and registration, and is a prerequisite for any authenticated route (profile, expenses) since those routes need a way to identify the current user and a way to gate access when no one is logged in.

## Depends on
- Step 1 — Database setup (`database/db.py` schema: `users` table with `id`, `name`, `email`, `password_hash`, `created_at`).
- Step 2 — Registration (creates the `users` rows that login authenticates against; established the session-based login pattern with `session["user_id"]`).

## Routes
- `GET /login` — renders the login form — public (already exists, no change to method needed)
- `POST /login` — validates input, looks up user by email, verifies password hash, starts a session, redirects to profile — public
- `GET /logout` — clears the session and redirects to landing page — logged-in (works even if session is already empty; no error if visited while logged out)

## Database changes
No database changes. The existing `users` table in `database/db.py` (`id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, created_at TEXT DEFAULT (datetime('now'))`) already supports login as-is.

## Templates
- **Create:** none
- **Modify:** `templates/login.html` — add server-rendered error handling for: missing fields and invalid credentials (wrong email or wrong password — use one generic message for both to avoid leaking which part was wrong). Repopulate the submitted `email` value on validation failure so the user doesn't retype it (matching the pattern in `register.html`). No structural/CSS changes needed — reuse the existing `auth-error` block already present.

## Files to change
- `app.py` — implement `POST` handling on the `/login` route: read form data, validate presence, look up user by email via `get_db()`, verify password with `check_password_hash`, set `session["user_id"]`, redirect to `/profile`. Implement `/logout`: clear the session (`session.clear()` or `session.pop("user_id", None)`) and redirect to `landing`.
- `templates/login.html` — repopulate submitted `email` value on error; ensure `auth-error` block renders the new validation/auth-failure messages.

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` (already available alongside `generate_password_hash`, already used in `database/db.py` and `app.py`) verifies the password. Flask's built-in `session` covers login/logout state.

## Rules for implementation
- No SQLAlchemy or ORMs — use `sqlite3` via `database.db.get_db()` only.
- Parameterised queries only — never interpolate/format user input into SQL strings.
- Passwords hashed with werkzeug — never compare or store plaintext passwords; use `check_password_hash` against the stored `password_hash`.
- Use CSS variables — never hardcode hex values in any CSS/inline styles touched.
- All templates extend `base.html`.
- Use one generic error message (e.g. "Invalid email or password.") for both "email not found" and "wrong password" cases — do not reveal which one failed.
- Validate that email and password are both present server-side even though the HTML form has `required` — client-side validation is not trustworthy.
- `/logout` must not error if called with no active session (e.g. a user who is already logged out visits it directly).

## Definition of done
- [ ] Visiting `/login` shows the existing login form unchanged in layout.
- [ ] Submitting the seeded demo user's credentials (`demo@spendly.com` / `demo123`) logs in successfully and redirects to `/profile`.
- [ ] Submitting a correct email with a wrong password re-renders the form with a generic "Invalid email or password." error and does not start a session.
- [ ] Submitting an email that doesn't exist in `users` re-renders the form with the same generic error and does not start a session.
- [ ] Submitting with a missing email or password re-renders the form with an error and does not start a session.
- [ ] Previously entered email is preserved in the form field after a validation or auth error.
- [ ] Visiting `/logout` while logged in clears the session and redirects to the landing page (`/`).
- [ ] Visiting `/logout` while logged out does not error and redirects to the landing page.
- [ ] No plaintext password ever appears in a redirect, query string, or log output.
