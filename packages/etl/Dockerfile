# packages/etl/Dockerfile

FROM python:3.11-slim

# 1) Set working directory
WORKDIR /app

# 2) Install OS‐level deps if needed (e.g. for psycopg2)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# 3) Copy and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copy your application code
COPY src/ ./src

# 5) Default command: run your CLI
ENTRYPOINT ["python", "-m", "src.main"]
