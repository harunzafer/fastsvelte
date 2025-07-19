-- Deploy fastsvelte:003_email_verification to pg

BEGIN;

CREATE TABLE IF NOT EXISTS fastsvelte.email_verification_token (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES fastsvelte."user"(id) ON DELETE CASCADE,
    token TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL,
    used_at TIMESTAMPTZ
);

COMMIT;
