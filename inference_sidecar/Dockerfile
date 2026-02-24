FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for building llama-cpp if needed
RUN apt-get update && apt-get install -y 
    build-essential 
    cmake 
    python3-dev 
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default model path if none provided via environment
ENV MODEL_PATH=/app/models/qwen2.5-1.5b-schema-guardian.gguf

EXPOSE 8000

# Use uvicorn to run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
