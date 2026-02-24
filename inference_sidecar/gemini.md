# Gemini CLI: Inference Sidecar Context

## Purpose
FastAPI serving the quantized Llama-3 GGUF model via `llama-cpp-python`.

## Tasks
- **FastAPI App (app.py):** Main API for synchronous classification.
- **Warmup Logic:** Ensure context is warm and model is ready before handling requests.
- **Latency Instrumentation:** Tracking and logging inference time (target < 50ms).
- **Caching/Forced Output:** Single-token classification to minimize generation time.

## Key Files
- `app.py`: FastAPI server.
- `requirements.txt`: Sidecar dependencies (`fastapi`, `uvicorn`, `llama-cpp-python`).
- `models/`: Directory for GGUF model files.
- `test_client.py`: Minimal Python test client.

## API Endpoint (Draft)
- **POST /validate:** JSON body -> LLM classification -> "SAFE" or "FLAGGED".
- **GET /health:** Health check with warmup status.
