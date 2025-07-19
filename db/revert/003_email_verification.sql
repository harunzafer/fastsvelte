-- Revert fastsvelte:003_email_verification from pg

BEGIN;

DROP TABLE IF EXISTS fastsvelte.email_verification_token;

COMMIT;
