# Schema-Guardian: Architecture Document

## Overview
A production-ready system for financial JSON message validation using local-first LLM classification.

## Data Flow
1. **Producer:** Financial systems publish ISO 20022-like JSON messages to Kafka.
2. **Consumer (Spring Boot):** Listens to Kafka topics, parses JSON, and performs initial structure check.
3. **Inference (FastAPI Sidecar):** Spring Boot sends the message body to the FastAPI sidecar.
4. **Classification (Llama-3 GGUF):** The sidecar uses `llama.cpp` to classify the message as "SAFE" or "FLAGGED".
5. **Routing (Spring Boot):**
   - **SAFE:** Message persists to PostgreSQL (production database).
   - **FLAGGED:** Message is routed to a Dead Letter Queue (DLQ) or Audit log.

## Components
- **Message Broker:** Kafka (KRaft mode).
- **Backend Service:** Spring Boot (Java 17/21).
- **Model Sidecar:** FastAPI + `llama-cpp-python` (GGUF model).
- **Persistence:** PostgreSQL for valid data.
- **ML Pipeline:** Unsloth (Fine-tuning) + QLoRA + llama.cpp (Quantization).

## Latency Target
- **< 50ms per inference.**
- Achievement strategies: Single-token output, model quantization (4-bit/5-bit), prompt caching, and potential GPU acceleration.
