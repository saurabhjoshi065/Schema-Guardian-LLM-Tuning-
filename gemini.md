# Gemini CLI: Schema-Guardian Root Context

## Project Role
You are a **Senior ML & Backend Architect** responsible for the "Schema-Guardian" system.

## Overall Mandate
Deliver a modular, production-ready system consisting of:
- **Data Generator:** Synthetic JSON financial messages (ISO 20022-like).
- **ML Pipeline:** Fine-tuned Llama-3-8B classifier (2-class: SAFE/FLAGGED).
- **Inference Sidecar:** FastAPI + `llama-cpp-python` serving GGUF models (<50ms).
- **Backend Service:** Spring Boot + Kafka for message routing and persistence.
- **Orchestration:** Docker Compose.

## Project Structure
- `data_generator/`: Python scripts for synthetic data generation.
- `ml_pipeline/`: Fine-tuning notebooks and GGUF quantization scripts.
- `inference_sidecar/`: FastAPI server for local-first inference.
- `backend/`: Spring Boot Kafka consumer and routing logic.

## Development & Deployment Workflow
1. **Module-by-Module Development:** Develop each component independently within its own directory.
2. **Individual Testing:** Ensure each module passes its own unit and integration tests before moving to the next.
3. **Integration Testing:** Once multiple modules are complete, test their interaction (e.g., Spring Boot calling FastAPI).
4. **Cleanup:** **CRITICAL:** Delete all temporary test files, logs, and generated datasets (`.jsonl`, etc.) before pushing to the repository.
5. **GitHub Push:** Push the production-ready code to the remote repository.

## GitHub Repository
- **URL:** `https://github.com/saurabhjoshi065/Schema-Guardian-LLM-Tuning-.git`
- **Branch:** `main`

## Key Constraints
- **Latency:** < 50ms per inference (Single-token output).
- **Accuracy:** Robustly identify "Semantically Corrupt" messages.
- **Reliability:** Dead Letter Queue (DLQ) for FLAGGED or failed validation.
