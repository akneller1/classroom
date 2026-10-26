# Student assignments: implementation and security boundary

## Shipped on this branch: Phase 1 (student focus view)

From an existing activity viewer page, select **Copy student link**. This produces `activity.html?path=<encoded-path>&student=1`. The student viewer removes the navigation, original-file shortcut, teacher answer-key link and report link. The standard teacher-facing activity view remains unchanged.

**This is presentation-only.** The repository and all of its published HTML, JavaScript, PDF files and answer keys are publicly accessible on GitHub Pages. Students can remove `student=1`, navigate directly to known URLs, use the iframe's own navigation, or inspect publicly served code. Do not use this mode to secure tests or confidential answers.

## Phase 2: secure assignment architecture (not yet deployed)

Requires a separate application/backend with server-side access enforcement (e.g. Supabase Auth + Postgres Row Level Security + serverless API), plus a protected storage location for teacher-only files and solutions. GitHub Pages can remain the marketing/public site but must not publish protected generators, answer keys, test questions, or private assignment data.

### Data model

- `teachers(id, auth_user_id, created_at)`
- `activities(id, title, kind, public_preview_url, protected_content_ref)`
- `assignments(id, teacher_id, activity_id, access_token_hash, config_json, starts_at, expires_at, revoked_at, created_at)`
- `attempts(id, assignment_id, student_alias, submitted_at, answers_json, score)`

### Authorization requirements

- Teacher routes and generator APIs require a verified authenticated teacher session.
- Assignment tokens must be high-entropy, randomly generated on the server, stored only as hashes, scoped to one assignment, revocable and checked server-side on every read and submit.
- Public student assignment endpoints return only student-safe problem data and permitted feedback. Never send full solution banks or teacher answer keys in JavaScript, HTML, PDFs or API payloads.
- Expiration and revocation must be checked server-side; hiding a button is not enforcement.
- Protect API calls and file downloads separately. Do not embed public GitHub Pages files if those files contain confidential material.
- If students enter names or responses, define retention, privacy notice and school approval before enabling collection. Start without student identity storage.
- Rate-limit token and attempt endpoints; set restrictive CORS and CSP, and log administrative actions without storing answers in logs.

### Migration and rollout

1. Inventory all public teacher-only assets and generator/answer-key routes.
2. Provision backend, auth provider, private storage, secrets and environment configuration.
3. Migrate sensitive content out of the public repository and history/exposed hosting, rotating any shared teacher codes.
4. Implement teacher dashboard, assignment creation, student-safe rendering, expiration and revocation.
5. Add integration tests for unauthorized direct URLs, expired/revoked tokens, teacher/assignment cross-access, answer leakage and direct file fetches.
6. Replace Phase 1 copy links with server-issued assignment URLs only after security tests pass.

No backend, authentication, protected content migration or server-enforced assignment access has been implemented by this branch.
