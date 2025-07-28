-- Deploy fastsvelte:006_update_organization_table to pg

BEGIN;

ALTER TABLE IF EXISTS fastsvelte.organization
ADD COLUMN IF NOT EXISTS first_seen_at TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS onboarding_complete_at TIMESTAMPTZ;


COMMIT;
