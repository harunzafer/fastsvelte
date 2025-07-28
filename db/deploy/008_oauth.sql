-- Deploy fastsvelte:008_oauth to pg

BEGIN;

-- Allow password_hash to be NULL for OAuth-only users
ALTER TABLE IF EXISTS fastsvelte."user"
    ALTER COLUMN password_hash DROP NOT NULL;

-- Add avatar_url column (optional)
ALTER TABLE IF EXISTS fastsvelte."user"
    ADD COLUMN IF NOT EXISTS avatar_url TEXT;

-- Create oauth_account table
CREATE TABLE IF NOT EXISTS fastsvelte.oauth_account (
    provider_id TEXT NOT NULL,
    provider_user_id TEXT NOT NULL,
    user_id INT NOT NULL REFERENCES fastsvelte."user"(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (provider_id, provider_user_id)
);


COMMIT;
