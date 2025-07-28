-- Revert fastsvelte:006_update_organization_table from pg

BEGIN;

ALTER TABLE IF EXISTS fastsvelte.organization
DROP COLUMN IF EXISTS onboarding_complete_at,
DROP COLUMN IF EXISTS first_seen_at;


COMMIT;
