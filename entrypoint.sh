#!/bin/sh
#
# wait for the database to be ready
python /app/wait-for-db.py

# check the exit code of the wait script
# if it's not 0 (success), then exit the container.
if [ $? -ne 0 ]; then
  echo "Could not connect to database. Exiting."
  exit 1
fi

# run database migrations
echo "Running database migrations..."
alembic upgrade head
psql "$DB_URL" -f /app/init.sql

# run the data seeding script
echo "Seeding initial data..."
python /app/seed_data.py

echo "Starting Gunicorn server..."
exec "$@"
