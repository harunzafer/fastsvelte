-- Deploy fastsvelte:002_basic_tables to pg

BEGIN;

CREATE TABLE IF NOT EXISTS fastsvelte.organization (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS fastsvelte.role (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS fastsvelte."user" (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    email_verified BOOLEAN DEFAULT FALSE,
    email_verified_at TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE,
    deleted_at TIMESTAMPTZ DEFAULT NULL,
    organization_id INT NOT NULL REFERENCES fastsvelte.organization(id) ON DELETE CASCADE,
    role_id INT REFERENCES fastsvelte.role(id),
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    CHECK (deleted_at IS NULL OR is_active = FALSE)
);

CREATE TABLE IF NOT EXISTS fastsvelte.session (
    id TEXT PRIMARY KEY,  -- ULID
    user_id INT NOT NULL REFERENCES fastsvelte."user"(id) ON DELETE CASCADE,
    context JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS fastsvelte.password_reset (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES fastsvelte."user"(id) ON DELETE CASCADE,
    token TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL,
    used_at TIMESTAMPTZ,
    attempts INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS fastsvelte.organization_setting_definition (
    id SERIAL PRIMARY KEY,
    key TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL CHECK (type IN ('string', 'boolean', 'int', 'float', 'json')),
    description TEXT
);

CREATE TABLE IF NOT EXISTS fastsvelte.user_setting_definition (
    id SERIAL PRIMARY KEY,
    key TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL CHECK (type IN ('string', 'boolean', 'int', 'float', 'json')),
    description TEXT
);

CREATE TABLE IF NOT EXISTS fastsvelte.organization_setting (
    id SERIAL PRIMARY KEY,
    organization_id INT NOT NULL REFERENCES fastsvelte.organization(id) ON DELETE CASCADE,
    definition_id INT NOT NULL REFERENCES fastsvelte.organization_setting_definition(id) ON DELETE CASCADE,
    value TEXT NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (organization_id, definition_id)
);

CREATE TABLE IF NOT EXISTS fastsvelte.user_setting (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES fastsvelte."user"(id) ON DELETE CASCADE,
    definition_id INT NOT NULL REFERENCES fastsvelte.user_setting_definition(id) ON DELETE CASCADE,
    value TEXT NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (user_id, definition_id)
);

CREATE TABLE IF NOT EXISTS fastsvelte.note (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES fastsvelte."user"(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS fastsvelte.event_log (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES fastsvelte."user"(id) ON DELETE SET NULL,
    organization_id INT REFERENCES fastsvelte.organization(id) ON DELETE SET NULL,
    session_id TEXT REFERENCES fastsvelte.session(id) ON DELETE SET NULL,
    event_type TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    ip_address TEXT,
    user_agent TEXT,
    request_path TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS fastsvelte.pricing (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    price_cents INT NOT NULL DEFAULT 0,
    billing_period TEXT NOT NULL CHECK (billing_period IN ('monthly', 'yearly', 'one_time')),
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS fastsvelte.organization_pricing (
    id SERIAL PRIMARY KEY,
    organization_id INT NOT NULL REFERENCES fastsvelte.organization(id) ON DELETE CASCADE,
    pricing_id INT NOT NULL REFERENCES fastsvelte.pricing(id),
    started_at TIMESTAMPTZ DEFAULT now(),
    expires_at TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE
);

-- Seed roles
INSERT INTO fastsvelte.role (name, description)
VALUES 
    ('sys_admin', 'Full access to manage users and settings across all organizations'),
    ('org_admin', 'Organization administrator with access to organization settings'),
    ('member', 'Standard user with access to core features'),
    ('readonly', 'User with read-only access to notes and settings'),
    ('cron', 'Cron job user with no UI access')    
ON CONFLICT (name) DO NOTHING;

-- Seed pricing plans
INSERT INTO fastsvelte.pricing (name, description, price_cents, billing_period, is_active, metadata)
VALUES
    ('Free', 'Free tier with basic usage limits', 0, 'one_time', TRUE, '{"max_notes": 10, "enable_ai": false}'),
    ('Pro Monthly', 'Pro tier with extended features', 2000, 'monthly', TRUE, '{"max_notes": 1000, "enable_ai": true}'),
    ('Pro Yearly', 'Discounted yearly plan', 20000, 'yearly', TRUE, '{"max_notes": 1000, "enable_ai": true}')
ON CONFLICT (name) DO NOTHING;

-- Seed test organization and capture its ID
WITH org_seed AS (
    INSERT INTO fastsvelte.organization (name)
    VALUES ('Local Test Org')
    RETURNING id
)

-- Seed admin user for that org
INSERT INTO fastsvelte."user" (
    email, password_hash, first_name, last_name, email_verified,
    is_active, organization_id, role_id, created_at, updated_at
)
SELECT 
    'admin@example.com',
    '$2b$12$XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',  -- bcrypt hash
    'Admin', 'User', TRUE,
    TRUE, org_seed.id, r.id,
    now(), now()
FROM org_seed
JOIN fastsvelte.role r ON r.name = 'admin';

-- Assign pricing plan to org
WITH org_seed AS (
    SELECT id FROM fastsvelte.organization WHERE name = 'Local Test Org'
)
INSERT INTO fastsvelte.organization_pricing (
    organization_id, pricing_id, started_at, is_active
)
SELECT 
    org_seed.id,
    p.id,
    now(), TRUE
FROM org_seed
JOIN fastsvelte.pricing p ON p.name = 'Free';


-- Seed organization setting definitions
INSERT INTO fastsvelte.organization_setting_definition (key, type, description)
VALUES
    ('allow_external_sharing', 'boolean', 'Allow users to share content externally'),
    ('default_note_visibility', 'string', 'Default visibility for new notes')
ON CONFLICT (key) DO NOTHING;

-- Seed user setting definitions
INSERT INTO fastsvelte.user_setting_definition (key, type, description)
VALUES
    ('theme', 'string', 'UI theme: light or dark'),
    ('notifications_enabled', 'boolean', 'Enable email notifications')
ON CONFLICT (key) DO NOTHING;


COMMIT;
