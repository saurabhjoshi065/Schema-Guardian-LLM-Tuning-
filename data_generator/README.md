# Data Generator

This module generates synthetic financial messages (ISO 20022-like) for training and testing the Schema-Guardian model.

## Features
- **Faker Integration:** Generates realistic IDs, IBANs, amounts, and dates.
- **Labeled Classes:**
  - `SAFE`: Valid financial messages.
  - `FLAGGED`: Semantically corrupt messages (negative amounts, future dates, invalid currency codes, etc.) that are still syntactically correct JSON.
- **JSON Schema Validation:** Includes a validator to ensure messages conform to the structural requirements.

## Files
- `generate.py`: Main script to generate the synthetic dataset.
- `validate_data.py`: Script to validate the generated dataset against `schema.json`.
- `schema.json`: The JSON schema defining the message structure.
- `requirements.txt`: Python dependencies.

## Setup and Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Generate the dataset:
   ```bash
   python generate.py
   ```
3. Validate the dataset:
   ```bash
   python validate_data.py
   ```

## Output
The generator produces `dataset.jsonl` with the following structure:
```json
{"label": "SAFE", "message": {"transaction_id": "...", "amount": 100.0, "currency": "USD", ...}}
```
