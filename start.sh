#!/bin/bash
set -e

echo "🚀 Starting TEF Website"
echo "======================="

echo "🔧 Using external PostgreSQL database"

# Auto-run database migrations (safe to run multiple times)
echo "📊 Checking database migrations..."
flask db upgrade || echo "⚠️  Migration failed or already up to date"

# Create admin user if doesn't exist (safe to run multiple times)
echo "👤 Checking admin user..."
python -c "
from pkg.models import db, Admin
from pkg import app

with app.app_context():
    existing = Admin.query.filter_by(email='hello@tosineniolorundafoundation.com').first()
    if not existing:
        admin = Admin(
            email='hello@tosineniolorundafoundation.com',
            password='scrypt:32768:8:1\$VA4acqcH8l6eyJlt\$c8d7a3aa2d7c881f61917989d6481597d26907be2cf6a8ce664bd2981260612da8ed9e01f6e6f31d505230657ffe0566015f0b24f0c9456cc439504478cd86dc'
        )
        db.session.add(admin)
        db.session.commit()
        print('✅ Admin user created')
    else:
        print('✅ Admin user already exists')
" || echo "⚠️  Admin check failed"

echo "✅ Setup complete!"
echo "🚀 Starting Flask application..."
echo ""

# Start supervisor to run Flask app
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
