# Schema-Guardian: Development Plan

## Phase 1: Data Generation (MVP 1)
- **Goal:** Create synthetic dataset for training and validation.
- **Tasks:**
  - Python script (`data_generator/generate.py`) using `Faker`.
  - Introduce "Semantically Corrupt" ISO 20022 messages (valid JSON, invalid logic).
  - Output: `dataset.jsonl` and `schema.json`.

## Phase 2: ML & Inference Sidecar (MVP 2)
- **Goal:** Fine-tune and serve the model.
- **Tasks:**
  - Fine-tuning notebook (`ml_pipeline/finetune_llama3_8b.ipynb`) using Unsloth + QLoRA.
  - GGUF export scripts and documentation.
  - FastAPI sidecar (`inference_sidecar/app.py`) with `llama-cpp-python`.
  - Latency instrumentation and single-token classification.

## Phase 3: Backend Integration (MVP 3)
- **Goal:** End-to-end message routing.
- **Tasks:**
  - Spring Boot app (`backend/`) with Java 17/21.
  - Kafka consumer for financial messages.
  - HTTP client to FastAPI sidecar for validation.
  - PostgreSQL persistence for "SAFE" and Kafka DLQ for "FLAGGED".

## Phase 4: Orchestration & Polishing
- **Goal:** Full system deployment.
- **Tasks:**
  - `docker-compose.yml` (Kafka KRaft, PostgreSQL, FastAPI, Spring Boot).
  - Module-level `README.md` documentation.
  - Performance profiling for < 50ms latency target.
