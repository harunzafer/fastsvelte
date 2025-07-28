-- Deploy fastsvelte:005_plan_and_usage.sql to pg

BEGIN;

-- Rename pricing to plan
ALTER TABLE IF EXISTS fastsvelte.pricing RENAME TO plan;

ALTER TABLE IF EXISTS fastsvelte.organization
    ADD COLUMN IF NOT EXISTS stripe_customer_id TEXT UNIQUE;

-- Remove unused columns from plan
ALTER TABLE IF EXISTS fastsvelte.plan
    DROP COLUMN IF EXISTS billing_period,
    DROP COLUMN IF EXISTS price_cents;

-- Rename metadata to features
ALTER TABLE IF EXISTS fastsvelte.plan
    RENAME COLUMN metadata TO features;

-- Add Stripe product ID and timestamps
ALTER TABLE IF EXISTS fastsvelte.plan
    ADD COLUMN IF NOT EXISTS stripe_product_id TEXT UNIQUE,
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT now(),
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT now();

-- Rename organization_pricing to organization_plan
ALTER TABLE IF EXISTS fastsvelte.organization_pricing RENAME TO organization_plan;

ALTER TABLE IF EXISTS fastsvelte.organization_plan
    RENAME COLUMN pricing_id TO plan_id;

-- Drop legacy columns
ALTER TABLE IF EXISTS fastsvelte.organization_plan
    DROP COLUMN IF EXISTS started_at,
    DROP COLUMN IF EXISTS expires_at,
    DROP COLUMN IF EXISTS is_active;

-- Add Stripe subscription tracking fields
ALTER TABLE IF EXISTS fastsvelte.organization_plan
    ADD COLUMN IF NOT EXISTS stripe_subscription_id TEXT UNIQUE,
    ADD COLUMN IF NOT EXISTS subscription_started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    ADD COLUMN IF NOT EXISTS current_period_starts_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS current_period_ends_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS ended_at TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS status TEXT,
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT now(),
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT now();

-- Create org_usage table to track monthly feature usage
CREATE TABLE IF NOT EXISTS fastsvelte.org_usage (
    id SERIAL PRIMARY KEY,
    organization_id INT NOT NULL REFERENCES fastsvelte.organization(id) ON DELETE CASCADE,
    feature_key TEXT NOT NULL,
    usage_count INT NOT NULL DEFAULT 0,
    period_start TIMESTAMPTZ NOT NULL,
    period_end TIMESTAMPTZ NOT NULL,
    UNIQUE (organization_id, feature_key, period_start)
);



-- Update seed plan rows to include Stripe product IDs and correct features
-- Normalize and update plan records to include features and Stripe product IDs
UPDATE fastsvelte.plan
SET
  stripe_product_id = CASE name
    WHEN 'Free' THEN 'prod_free_001'
    WHEN 'Pro' THEN 'prod_pro_001'
    WHEN 'Premium' THEN 'prod_premium_001'
    ELSE stripe_product_id
  END,
  features = CASE name
    WHEN 'Free' THEN '{"max_bots": 1, "storage_gb": 1, "enable_ai": false, "token_limit": 5000, "email_limit": 50}'
    WHEN 'Pro' THEN '{"max_bots": 10, "storage_gb": 50, "enable_ai": true, "token_limit": 100000, "email_limit": 1000}'
    WHEN 'Premium' THEN '{"max_bots": 25, "storage_gb": 200, "enable_ai": true, "token_limit": 500000, "email_limit": 5000}'
    ELSE features
  END
WHERE name IN ('Free', 'Pro', 'Premium');



COMMIT;
