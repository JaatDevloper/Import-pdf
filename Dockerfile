FROM python:3.11-slim

WORKDIR /app

# Install essential packages with Devanagari font support
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    fonts-noto \
    fonts-lohit-deva \
    locales \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && echo "hi_IN.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen

# Set environment variables for proper encoding
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV PYTHONIOENCODING=utf-8

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port for the health check server
EXPOSE 8080

# Start the bot
CMD ["python", "healthcheck.py"]
