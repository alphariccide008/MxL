# TEF Website - Docker Deployment

## Simple Docker Build & Run

This Dockerfile contains **everything** in one container:
- MySQL database
- Flask application
- All dependencies

### Build the Image

```bash
docker build -t tef-website .
```

### Run the Container

```bash
docker run -d -p 5000:5000 --name tef-app tef-website
```

### Access the Application

```
http://localhost:5000
```

---

## What's Inside

The Dockerfile automatically:
1. Installs MySQL server
2. Installs all Python dependencies
3. Initializes the database
4. Imports your database schema (moniepoint.sql)
5. Starts both MySQL and Flask app

**Everything runs in ONE container!**

---

## Commands

### Build
```bash
docker build -t tef-website .
```

### Run
```bash
docker run -d -p 5000:5000 --name tef-app tef-website
```

### View Logs
```bash
docker logs -f tef-app
```

### Stop
```bash
docker stop tef-app
```

### Remove
```bash
docker rm tef-app
```

### Restart
```bash
docker restart tef-app
```

---

## That's It!

No docker-compose needed. Just build and run! 🚀
