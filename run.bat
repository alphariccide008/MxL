@echo off
echo Stopping any existing tef-app container...
docker stop tef-app 2>nul
docker rm tef-app 2>nul

echo Starting TEF Website...
docker run -d -p 5000:5000 --name tef-app tef-website

echo.
echo TEF Website is starting...
echo Access it at: http://localhost:5000
echo.
echo View logs: docker logs -f tef-app
pause
