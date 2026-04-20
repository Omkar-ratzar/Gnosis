-- Create application databases
CREATE DATABASE gnosis_db OWNER airflow;
CREATE DATABASE airflow_db OWNER airflow;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE gnosis_db TO airflow;
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow;

\connect gnosis_db;

CREATE TABLE IF NOT EXISTS all_files (
    file_id SERIAL PRIMARY KEY,
    file_path VARCHAR(1024) UNIQUE NOT NULL,
    file_status VARCHAR(20) NOT NULL DEFAULT 'NEW',
    last_modified TIMESTAMP
    user_id INT REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS image_metadata (
    id SERIAL PRIMARY KEY,
    file_id INT UNIQUE NOT NULL REFERENCES all_files(file_id),
    file_path VARCHAR(1024),
    description TEXT,
    exif JSONB,
    status VARCHAR(20) NOT NULL DEFAULT 'NEW'
);
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
