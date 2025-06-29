-- Verify fastsvelte:001_create_schema on pg

BEGIN;

SELECT pg_catalog.has_schema_privilege('fastsvelte', 'usage');

ROLLBACK;
