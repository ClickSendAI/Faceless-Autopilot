FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Create directories for generated content
RUN mkdir -p generated_content generated_audio

# Expose port
EXPOSE 8561

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8561"]
