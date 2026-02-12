# Use official Python image
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (Render injects $PORT)
EXPOSE 8000

# Run the FastAPI app (use $PORT for Render compatibility)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
