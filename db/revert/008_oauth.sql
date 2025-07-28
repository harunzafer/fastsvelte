-- Revert fastsvelte:008_oauth from pg

BEGIN;

-- Drop oauth_account table
DROP TABLE IF EXISTS fastsvelte.oauth_account;

-- Remove avatar_url column
ALTER TABLE IF EXISTS fastsvelte."user"
    DROP COLUMN IF EXISTS avatar_url;

-- Revert password_hash to NOT NULL
ALTER TABLE IF EXISTS fastsvelte."user"
    ALTER COLUMN password_hash SET NOT NULL;
    
COMMIT;
