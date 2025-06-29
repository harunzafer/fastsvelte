-- Revert fastsvelte:001_create_schema from pg

BEGIN;

DROP SCHEMA flipr;

COMMIT;
