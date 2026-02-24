# Schema-Guardian Backend (Spring Boot)

This module handles the ingestion, validation, and routing of financial messages.

## Features
- **Kafka Integration:** Listens to the `financial-messages-in` topic.
- **LLM Sidecar Client:** Forwards message content to the FastAPI sidecar for semantic classification.
- **Routing Logic:**
  - `SAFE`: Persists the message into PostgreSQL.
  - `FLAGGED`: Routes the message to the `financial-messages-flagged` (DLQ) Kafka topic.
- **Error Handling:** If the sidecar is unreachable, the message is automatically flagged and sent to the DLQ for audit.

## Setup
1. **Dependencies:** Java 17+, Maven.
2. **Environment Variables:**
   - `KAFKA_BOOTSTRAP_SERVERS`: Kafka broker address (default: `localhost:9092`).
   - `POSTGRES_HOST`: Database address (default: `localhost:5432`).
   - `SIDECAR_URL`: FastAPI endpoint (default: `http://localhost:8000/validate`).

## Running
```bash
cd backend
mvn spring-boot:run
```

## Architecture Notes
The backend uses a synchronous call to the LLM sidecar. Given our **< 50ms** target in the sidecar, this design maintains low overall latency while ensuring strict data integrity before persistence.
