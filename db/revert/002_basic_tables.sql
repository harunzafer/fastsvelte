-- Revert fastsvelte:002_basic_tables from pg

BEGIN;

DROP TABLE IF EXISTS fastsvelte.organization_pricing;
DROP TABLE IF EXISTS fastsvelte.pricing;
DROP TABLE IF EXISTS fastsvelte.event_log;
DROP TABLE IF EXISTS fastsvelte.note;
DROP TABLE IF EXISTS fastsvelte.user_setting;
DROP TABLE IF EXISTS fastsvelte.organization_setting;
DROP TABLE IF EXISTS fastsvelte.user_setting_definition;
DROP TABLE IF EXISTS fastsvelte.organization_setting_definition;
DROP TABLE IF EXISTS fastsvelte.password_reset;
DROP TABLE IF EXISTS fastsvelte.session;
DROP TABLE IF EXISTS fastsvelte."user";
DROP TABLE IF EXISTS fastsvelte.role;
DROP TABLE IF EXISTS fastsvelte.organization;

COMMIT;
