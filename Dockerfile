FROM python:3.11-slim

WORKDIR /app

# Install essential packages including Hindi fonts
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    fonts-noto-cjk \
    fonts-noto \
    fonts-freefont-ttf \
    fonts-indic \
    fonts-lohit-deva \
    fonts-nakula \
    fonts-gargi \
    fonts-sarai \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port for the health check server
EXPOSE 8080

# Start the bot
CMD ["python", "healthcheck.py"]
