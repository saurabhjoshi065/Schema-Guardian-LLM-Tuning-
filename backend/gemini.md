# Gemini CLI: Spring Boot Backend Context

## Purpose
Robust message routing and persistence for Schema-Guardian.

## Tasks
- **Spring Boot App:** Java 17/21 backend.
- **Kafka Listener:** `@KafkaListener` to consume messages from financial topics.
- **Service Client:** Synchronous calls to the FastAPI sidecar.
- **PostgreSQL Persistence:** Saving "SAFE" messages to a production table.
- **DLQ/Audit:** Routing "FLAGGED" or failed messages to a Kafka DLQ topic.

## Key Files
- `src/main/java/`: Java source code for consumers, services, and models.
- `src/main/resources/`: Configuration properties (Kafka, DB, Sidecar URL).
- `pom.xml` / `build.gradle`: Project dependencies.
- `docker-compose.yml`: (Optional, but orchestration is coordinated here).

## Configuration (Draft)
- `spring.kafka.consumer.group-id=schema-guardian-group`
- `schema-guardian.sidecar.url=http://inference-sidecar:8000/validate`
- `spring.datasource.url=jdbc:postgresql://postgres:5432/guardian_db`
