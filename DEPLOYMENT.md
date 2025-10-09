# TEF Website - Deployment Guide

## Quick Start (Any Computer)

### Prerequisites
- Docker installed
- Internet connection (to reach Render PostgreSQL)

### Deploy in 3 Commands

```bash
# 1. Build the Docker image
docker build -t tef-app .

# 2. Run the container
docker run -d -p 5000:5000 --name tef-container tef-app

# 3. Access the application
# Open browser: http://localhost:5000
```

That's it! The container will automatically:
- ✅ Run database migrations
- ✅ Create admin user if needed
- ✅ Start the Flask application

## What Happens on Startup

The startup script ([start.sh](start.sh)) automatically:

1. **Checks Database Migrations** - Runs `flask db upgrade` (safe to run multiple times)
2. **Checks Admin User** - Creates admin if doesn't exist (safe to run multiple times)
3. **Starts Application** - Launches Gunicorn with 2 workers

## Database Connection

The application connects to **PostgreSQL on Render.com**:

- **Host:** dpg-d3jnsrl6ubrc73d02nsg-a.oregon-postgres.render.com
- **Port:** 5432
- **Database:** moniepoint
- **User:** moniepoint_user

**Important:** The database is shared across all deployments. Data persists regardless of where you run the container.

## Admin Login

- **URL:** http://localhost:5000/admin/
- **Email:** hello@tosineniolorundafoundation.com
- **Password:** (your admin password)

## Useful Commands

```bash
# View logs
docker logs tef-container

# Follow logs in real-time
docker logs -f tef-container

# Check database
docker exec tef-container python check_db.py

# Stop container
docker stop tef-container

# Start container again
docker start tef-container

# Restart container
docker restart tef-container

# Remove container (data stays in Render DB)
docker stop tef-container && docker rm tef-container

# Rebuild after code changes
docker build -t tef-app .
docker stop tef-container && docker rm tef-container
docker run -d -p 5000:5000 --name tef-container tef-app
```

## Deploy to Different Environments

### Production Server
Same commands work on any Linux server with Docker installed.

### Cloud Platforms

**Render.com:**
```bash
# Connect your GitHub repo
# Render will auto-detect Dockerfile
# Set port to 5000
```

**AWS/Azure/GCP:**
```bash
# Push to container registry
docker tag tef-app your-registry/tef-app
docker push your-registry/tef-app

# Deploy using their container services
```

## Troubleshooting

### Container won't start
```bash
docker logs tef-container
```

### Database connection error
- Check internet connection
- Verify Render PostgreSQL is running
- Check credentials in [Dockerfile](Dockerfile:47)

### Port already in use
```bash
# Use a different port
docker run -d -p 8000:5000 --name tef-container tef-app
# Access at http://localhost:8000
```

## Migration from MySQL to PostgreSQL

This application was migrated from MySQL to PostgreSQL. Key changes:
- ✅ Database driver: `psycopg2-binary` instead of `mysql-connector`
- ✅ Connection string: `postgresql://` instead of `mysql+mysqlconnector://`
- ✅ Models: Compatible with both (using SQLAlchemy)
- ✅ No MySQL server in container (external PostgreSQL on Render)

## Need Help?

Check these files:
- [Dockerfile](Dockerfile) - Container configuration
- [start.sh](start.sh) - Startup automation script
- [pkg/docker_config.py](pkg/docker_config.py) - Database configuration
- [requirements.txt](requirements.txt) - Python dependencies
