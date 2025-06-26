# Use a slim Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install required system packages: ffmpeg and curl
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy bot files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Write cookies from environment variable (optional for Koyeb)
# Assumes you set a Koyeb Secret named "COOKIES"
RUN if [ ! -z "$COOKIES" ]; then echo "$COOKIES" > /app/cookies.txt; fi

# Expose ENV to yt-dlp and utils
ENV COOKIES_PATH=/app/cookies.txt

# Run the bot
CMD ["python", "main.py"]
