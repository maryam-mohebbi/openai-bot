# Dockerfile
FROM python:3.10

# Install MySQL client
RUN apt-get update \
    && apt-get install -y default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the src folder content to the /app directory in the container
COPY src /app

# Copy the mysql-entrypoint.sh to the /app directory in the container
COPY mysql-entrypoint.sh /app
RUN chmod +x mysql-entrypoint.sh

CMD ["./mysql-entrypoint.sh", "python", "main.py"]
