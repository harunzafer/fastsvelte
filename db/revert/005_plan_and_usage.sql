-- Revert fastsvelte:005_plan_and_usage.sql from pg

BEGIN;

-- Drop org_usage table
DROP TABLE IF EXISTS fastsvelte.org_usage;

ALTER TABLE IF EXISTS fastsvelte.organization
    DROP COLUMN IF EXISTS stripe_customer_id;

-- Drop organization_plan columns
ALTER TABLE IF EXISTS fastsvelte.organization_plan
    DROP COLUMN IF EXISTS stripe_subscription_id,
    DROP COLUMN IF EXISTS subscription_started_at,
    DROP COLUMN IF EXISTS current_period_starts_at,
    DROP COLUMN IF EXISTS current_period_ends_at,
    DROP COLUMN IF EXISTS ended_at,
    DROP COLUMN IF EXISTS status,
    DROP COLUMN IF EXISTS created_at,
    DROP COLUMN IF EXISTS updated_at;

-- Rename organization_plan back to organization_pricing
ALTER TABLE IF EXISTS fastsvelte.organization_plan RENAME TO organization_pricing;

-- Drop new plan columns
ALTER TABLE IF EXISTS fastsvelte.plan
    DROP COLUMN IF EXISTS stripe_product_id,
    DROP COLUMN IF EXISTS created_at,
    DROP COLUMN IF EXISTS updated_at;

-- Rename features back to metadata
ALTER TABLE IF EXISTS fastsvelte.plan
    RENAME COLUMN IF EXISTS features TO metadata;

-- Re-add dropped pricing columns
ALTER TABLE IF EXISTS fastsvelte.plan
    ADD COLUMN IF NOT EXISTS billing_period TEXT NOT NULL DEFAULT 'monthly',
    ADD COLUMN IF NOT EXISTS price_cents INT NOT NULL DEFAULT 0;

-- Rename plan back to pricing
ALTER TABLE IF EXISTS fastsvelte.plan RENAME TO pricing;

-- Restore original seed data
DELETE FROM fastsvelte.pricing;

INSERT INTO fastsvelte.pricing (name, description, price_cents, billing_period, is_active, metadata)
VALUES
    ('Free', 'Free tier with basic usage limits', 0, 'one_time', TRUE, '{"max_notes": 10, "enable_ai": false}'),
    ('Pro Monthly', 'Pro tier with extended features', 2000, 'monthly', TRUE, '{"max_notes": 1000, "enable_ai": true}'),
    ('Pro Yearly', 'Discounted yearly plan', 20000, 'yearly', TRUE, '{"max_notes": 1000, "enable_ai": true}');

COMMIT;

