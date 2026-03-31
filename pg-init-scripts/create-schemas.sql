-- Ensure schema exists in the main (dev) database
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'clean_backend') THEN
        CREATE SCHEMA clean_backend;
    END IF;
END $$;

CREATE EXTENSION IF NOT EXISTS citext;

-- Create separate test database and schema (variant 1).
-- NOTE: CREATE DATABASE cannot run inside DO/transaction, so we use psql \gexec.
SELECT 'CREATE DATABASE backend_test'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'backend_test')\gexec

\connect backend_test

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'clean_backend') THEN
        CREATE SCHEMA clean_backend;
    END IF;
END $$;

CREATE EXTENSION IF NOT EXISTS citext;