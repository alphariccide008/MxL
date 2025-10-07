@echo off
echo Building TEF Website Docker image...
docker build -t tef-website .
echo.
echo Done! Now run: docker run -d -p 5000:5000 --name tef-app tef-website
pause
