FROM python:3.11-slim

WORKDIR /app

# Install essential packages including Hindi fonts and pdfplumber dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    fonts-noto-cjk \
    fonts-noto \
    fonts-indic \
    fonts-lohit-deva \
    fonts-gargi \
    build-essential \
    libpoppler-cpp-dev \
    pkg-config \
    python3-dev \
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
