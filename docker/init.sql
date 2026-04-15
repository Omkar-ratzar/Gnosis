-- Create application databases
CREATE DATABASE gnosis_db OWNER airflow;
CREATE DATABASE airflow_db OWNER airflow;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE gnosis_db TO airflow;
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow;
