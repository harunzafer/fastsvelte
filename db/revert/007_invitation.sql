-- Revert fastsvelte:007_invitation from pg

BEGIN;

DROP TABLE IF EXISTS fastsvelte.invitation;

COMMIT;
