FROM apache/airflow:3.2.0

USER root

# Install system dependency required by python-magic
RUN apt-get update && \
    apt-get install -y libmagic1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER airflow
COPY requirements.txt .

# Install Python dependency
RUN pip install --no-cache-dir -r requirements.txt
