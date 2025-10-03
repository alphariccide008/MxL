# TEFoundation Flask Application

A Flask web application with Docker support for easy deployment and development.

## Prerequisites

- Docker Desktop installed on your system
- Docker Compose (included with Docker Desktop)

## Quick Start with Docker

### 1. Clone and Navigate to Project
```bash
cd TEFoundation
```

### 2. Build and Run with Docker Compose
```bash
docker-compose up --build
```

This command will:
- Build the Flask application container
- Start a MySQL database container
- Set up networking between containers
- Make the app available at http://localhost:5000

### 3. Initialize Database (First Time Only)
In a new terminal, run:
```bash
docker-compose exec web flask db upgrade
```

## Docker Commands

### Start the application
```bash
docker-compose up
```

### Start in background (detached mode)
```bash
docker-compose up -d
```

### Stop the application
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs web
docker-compose logs db
```

### Rebuild containers (after code changes)
```bash
docker-compose up --build
```

### Access the web container shell
```bash
docker-compose exec web bash
```

### Access MySQL database
```bash
docker-compose exec db mysql -u root -p moniepoint
# Password: password
```

## Local Development (Without Docker)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up Local MySQL Database
- Install MySQL locally
- Create database named `moniepoint`
- Update connection details in `pkg/config.py`

### 3. Run Application
```bash
python starter.py
```

## Environment Variables

You can customize the Docker deployment using environment variables:

```bash
# Create .env file
DATABASE_URL=mysql+mysqlconnector://user:pass@db:3306/dbname
SECRET_KEY=your-secret-key
ADMIN_EMAIL=admin@example.com
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## File Structure

```
TEFoundation/
├── pkg/                    # Main application package
│   ├── static/            # Static files (CSS, JS, images)
│   ├── templates/         # HTML templates
│   ├── __init__.py        # App factory
│   ├── config.py          # Local development config
│   ├── docker_config.py   # Docker/production config
│   ├── models.py          # Database models
│   ├── forms.py           # WTForms
│   ├── admin_routes.py    # Admin routes
│   └── user_routes.py     # User routes
├── migrations/            # Database migrations
├── upload/               # File uploads directory
├── uploads/              # Additional uploads
├── Dockerfile            # Docker container definition
├── docker-compose.yml    # Multi-container setup
├── requirements.txt      # Python dependencies
├── starter.py           # Development server
└── wsgi.py              # Production WSGI entry point
```

## Database Migrations

### Create a new migration
```bash
docker-compose exec web flask db migrate -m "Description of changes"
```

### Apply migrations
```bash
docker-compose exec web flask db upgrade
```

## Troubleshooting

### Port Already in Use
If port 5000 or 3306 is already in use, modify the ports in `docker-compose.yml`:
```yaml
services:
  web:
    ports:
      - "8000:5000"  # Change 5000 to 8000
  db:
    ports:
      - "3307:3306"  # Change 3306 to 3307
```

### Database Connection Issues
1. Ensure MySQL container is running: `docker-compose ps`
2. Check database logs: `docker-compose logs db`
3. Verify database exists: `docker-compose exec db mysql -u root -p -e "SHOW DATABASES;"`

### Container Build Issues
1. Clear Docker cache: `docker system prune -a`
2. Rebuild without cache: `docker-compose build --no-cache`

## Production Deployment

For production deployment:

1. Update environment variables in `docker-compose.yml`
2. Use proper secrets management
3. Set up reverse proxy (nginx)
4. Configure SSL certificates
5. Set up database backups

## Support

For issues and questions, please check the application logs:
```bash
docker-compose logs -f web
```