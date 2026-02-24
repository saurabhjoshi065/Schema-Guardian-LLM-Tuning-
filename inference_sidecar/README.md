# Inference Sidecar: Llama-3-8B GGUF Server

This module provides the low-latency classification endpoint for Schema-Guardian.

## Features
- **FastAPI Endpoint:** `/validate` for real-time inference.
- **Quantized GGUF Serving:** Uses `llama-cpp-python` for high-performance inference on CPU/GPU.
- **Low Latency Target:** Forcing a single-token classification response ("SAFE" or "FLAGGED") to hit sub-50ms goals.
- **Warmup Logic:** Model loads and performs a dummy inference on startup to ensure high availability.

## Setup
1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Model Placement:**
    Place your fine-tuned and quantized Llama-3-8B GGUF model in the `models/` directory.
    - Path: `inference_sidecar/models/llama-3-8b-schema-guardian.gguf`

3.  **Run Server:**
    ```bash
    uvicorn app:app --host 0.0.0.0 --port 8000
    ```

## API Specification

### POST `/validate`
- **Request Body:**
    ```json
    {
        "message": {
            "transaction_id": "...",
            "amount": 100.0,
            "currency": "USD",
            ...
        }
    }
    ```
- **Response Body:**
    ```json
    {
        "label": "SAFE",
        "latency_ms": 42.5
    }
    ```

### GET `/health`
- Returns model load status and service health.

## Note on Performance
To achieve the **< 50ms** target, this sidecar uses:
- **Single-Token Decoding:** We only decode one token for classification.
- **Prompt Caching:** (Configurable) to reuse common instruction prefixes.
- **Deterministic Inference:** Temperature set to 0.0 for consistent classification.
