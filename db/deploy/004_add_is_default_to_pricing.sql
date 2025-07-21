-- Deploy fastsvelte:004_add_is_default_to_pricing to pg

BEGIN;

ALTER TABLE fastsvelte.pricing
ADD COLUMN IF NOT EXISTS is_default BOOLEAN DEFAULT FALSE;

-- Enforce only one default plan using a partial unique index
CREATE UNIQUE INDEX IF NOT EXISTS one_default_pricing_plan
ON fastsvelte.pricing (is_default)
WHERE is_default = TRUE;

-- Set 'Free' as the default
UPDATE fastsvelte.pricing
SET is_default = TRUE
WHERE name = 'Free';

COMMIT;
