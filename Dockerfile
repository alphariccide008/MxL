FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including PostgreSQL client and supervisor
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    pkg-config \
    wget \
    xfonts-75dpi \
    xfonts-base \
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
RUN mkdir -p upload uploads pkg/static/profiles

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy startup script and fix line endings
COPY start.sh /start.sh
RUN sed -i 's/\r$//' /start.sh && chmod +x /start.sh

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=production
ENV DATABASE_URL=postgresql://moniepointjournalism_5l5w_user:R0eDnbOKKgnYtelOLFdHRT76Tz6gGhnn@dpg-d4n9ep6uk2gs739ldcd0-a.oregon-postgres.render.com/moniepointjournalism_5l5w

# Run Flask app using supervisor
CMD ["/start.sh"]