FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including MySQL server and supervisor
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    wget \
    xfonts-75dpi \
    xfonts-base \
    default-mysql-server \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install wkhtmltopdf from official package
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.bookworm_amd64.deb && \
    apt-get update && \
    apt-get install -y ./wkhtmltox_0.12.6.1-3.bookworm_amd64.deb && \
    rm wkhtmltox_0.12.6.1-3.bookworm_amd64.deb && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p upload uploads pkg/static/profiles /var/run/mysqld /var/lib/mysql

# Set up MySQL
RUN chown -R mysql:mysql /var/lib/mysql /var/run/mysqld

# Copy database initialization SQL
COPY moniepoint.sql /docker-entrypoint-initdb.d/moniepoint.sql

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=production
ENV DATABASE_URL=mysql+mysqlconnector://root:password@localhost:3306/moniepoint

# Run both MySQL and Flask app using supervisor
CMD ["/start.sh"]