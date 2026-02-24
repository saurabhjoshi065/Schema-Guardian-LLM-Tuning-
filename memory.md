# Schema-Guardian: Memory & Context

## Key Project Facts
- **Objective:** Production-ready "Schema-Guardian" for ISO 20022-like JSON financial messages.
- **Tech Stack:**
  - **Backend:** Spring Boot (Java 17/21), Kafka.
  - **ML Frameworks:** Unsloth, QLoRA, llama.cpp.
  - **Serving:** FastAPI, `llama-cpp-python`.
  - **Database:** PostgreSQL.
  - **Orchestration:** Docker Compose (KRaft mode for Kafka).
- **Target Metrics:** < 50ms latency for classification.
- **Domain:** Synthetic financial data generation and classification (2-class: Clean vs. Semantically Corrupt).

## Decisions
- **Local-First Inference:** Using quantized Llama-3-8B GGUF for low latency and privacy.
- **KRaft Mode:** Using modern Kafka orchestration without Zookeeper.
- **Single-Token Classification:** Forcing LLM to output only "SAFE" or "FLAG" to minimize token generation time.

## Outstanding Items
- Fine-tuning the Llama-3-8B model on synthetic data.
- Quantizing the fine-tuned adapter/base model to GGUF format.
- Tuning Spring Boot's HTTP client for low-latency communication with the sidecar.
