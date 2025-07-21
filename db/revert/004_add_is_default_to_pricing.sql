-- Revert fastsvelte:004_add_is_default_to_pricing from pg

BEGIN;

DROP INDEX IF EXISTS fastsvelte.one_default_pricing_plan;
ALTER TABLE fastsvelte.pricing DROP COLUMN IF EXISTS is_default;

COMMIT;
