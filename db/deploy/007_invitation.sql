-- Deploy fastsvelte:007_invitation to pg

BEGIN;

CREATE TABLE IF NOT EXISTS fastsvelte.invitation (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL,
    token TEXT NOT NULL UNIQUE,
    role_name TEXT NOT NULL REFERENCES fastsvelte.role(name),
    organization_id INT REFERENCES fastsvelte.organization(id) ON DELETE CASCADE,
    created_by INT REFERENCES fastsvelte."user"(id),
    accepted_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

COMMIT;
