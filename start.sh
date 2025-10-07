#!/bin/bash
set -e

echo "🚀 Starting TEF Website (All-in-One Container)"
echo "=============================================="

# Initialize MySQL if not already initialized
if [ ! -d "/var/lib/mysql/mysql" ]; then
    echo "📦 Initializing MySQL database..."
    mysqld --initialize-insecure --user=mysql --datadir=/var/lib/mysql
fi

# Start MySQL temporarily to set up database
echo "🔧 Starting MySQL for setup..."
mysqld_safe --datadir=/var/lib/mysql &
MYSQL_PID=$!

# Wait for MySQL to be ready
echo "⏳ Waiting for MySQL to start..."
for i in {1..30}; do
    if mysqladmin ping -h localhost --silent; then
        echo "✅ MySQL is ready!"
        break
    fi
    echo "   Waiting... ($i/30)"
    sleep 2
done

# Create database and user
echo "📚 Setting up database..."
mysql -u root <<-EOSQL
    ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';
    CREATE DATABASE IF NOT EXISTS moniepoint;
    CREATE USER IF NOT EXISTS 'appuser'@'localhost' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON moniepoint.* TO 'appuser'@'localhost';
    GRANT ALL PRIVILEGES ON moniepoint.* TO 'root'@'localhost';
    FLUSH PRIVILEGES;
EOSQL

# Import SQL file if exists
if [ -f "/docker-entrypoint-initdb.d/moniepoint.sql" ]; then
    echo "📥 Importing database schema..."
    mysql -u root -ppassword moniepoint < /docker-entrypoint-initdb.d/moniepoint.sql
fi

# Stop temporary MySQL
echo "🔄 Stopping temporary MySQL..."
mysqladmin -u root -ppassword shutdown
wait $MYSQL_PID

echo "✅ Setup complete!"
echo "🚀 Starting all services..."
echo ""

# Start supervisor to run both MySQL and Flask app
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
