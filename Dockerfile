FROM python:3.11-slim

WORKDIR /app

# Install required packages including Hindi font support
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    fonts-freefont-ttf \
    fonts-noto \
    fonts-noto-cjk \
    locales \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up locale for Hindi support
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    sed -i -e 's/# hi_IN UTF-8/hi_IN UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Install Python dependencies
RUN pip install --no-cache-dir python-telegram-bot==13.15 Flask==2.3.3 PyPDF2==3.0.1 PyMuPDF==1.22.5 reportlab==4.0.4 psycopg2-binary==2.9.7 python-dotenv==1.0.0

# Copy the application code
COPY . .

# Expose the port for the health check server
EXPOSE 8080

# Start the bot
CMD ["python", "healthcheck.py"]
