# Dockerfile for Linux production with LibreOffice
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive


# Create app dir
WORKDIR /app

# Copy python requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app

# Create output dir
RUN mkdir -p /app/output /app/templates

# Expose port
EXPOSE 5000

# Run with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
