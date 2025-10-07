#!/bin/bash
set -e

echo "⏳ Waiting for MySQL to be ready..."

# Wait for MySQL to be ready
until mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" --skip-ssl -e "SELECT 1" >/dev/null 2>&1; do
  echo "❗ MySQL is unavailable - sleeping..."
  sleep 2
done

echo "✅ MySQL is ready!"

# Run database migrations
echo "🔄 Running database migrations..."
flask db upgrade || echo "⚠️  Migrations failed or not needed"

# Start the application
echo "🚀 Starting application..."
exec gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 wsgi:app
