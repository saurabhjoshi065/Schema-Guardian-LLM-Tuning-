# Gemini CLI: Data Generator Context

## Purpose
Synthetic generation of ISO 20022-like JSON financial messages.

## Tasks
- **generate.py:** Python script using `Faker`.
- **Target Size:** 5,000 synthetic JSON messages.
- **Labels:**
  - **Clean:** Valid JSON, valid logic.
  - **Semantically Corrupt:** Valid JSON structure, but logically invalid values (e.g., negative amounts, future settlement dates, invalid currency codes).
- **Outputs:** `dataset.jsonl` (for training) and `schema.json` (for structure validation).

## Key Files
- `generate.py`: Main generation logic.
- `requirements.txt`: Python dependencies (`faker`, `jsonlines`, etc.).
- `dataset.jsonl`: Output training data.
- `schema.json`: JSON schema for messages.
