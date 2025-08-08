#!/bin/sh

set -e

echo "Running database migrations..."
alembic upgrade head

echo "Applying triggers and functions..."
psql "$DB_URL" -f /app/init.sql

# better do this manually
# echo "Seeding initial data..."
# python /app/seed_data.py

echo "Release tasks complete!"
