#!/bin/bash

set -e

# Wait for the MySQL server to be ready
while ! mysqladmin ping -hdb --silent; do
    echo "Waiting for MySQL server to be ready..."
    sleep 2
done

# Check if the database already exists
if ! mysql -u${MYSQL_USER} -p${MYSQL_PASSWORD} -h db -e "USE ${MYSQL_DATABASE}"; then
    echo "Creating database schema from database.sql"
    mysql -u${MYSQL_USER} -p${MYSQL_PASSWORD} -h db ${MYSQL_DATABASE} < /docker-entrypoint-initdb.d/database.sql
else
    echo "Database already initialized"
fi

# Start the Python application
exec "$@"
