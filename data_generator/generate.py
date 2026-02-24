import json
import random
import uuid
from datetime import datetime, timedelta
from faker import Faker
import jsonlines

fake = Faker()

# Configuration
TOTAL_RECORDS = 5000
CLEAN_RATIO = 0.5
OUTPUT_FILE = "data_generator/dataset.jsonl"

def generate_clean_message():
    """Generates a semantically valid financial message."""
    return {
        "transaction_id": str(uuid.uuid4()),
        "amount": round(random.uniform(10.0, 10000.0), 2),
        "currency": fake.currency_code(),
        "sender_iban": fake.iban(),
        "receiver_iban": fake.iban(),
        "settlement_date": str(fake.date_between(start_date="-30d", end_date="today")),
        "status": random.choice(["PENDING", "COMPLETED", "SETTLED"])
    }

def generate_corrupt_message():
    """Generates a semantically invalid but syntactically correct message."""
    message = generate_clean_message()
    
    # Introduce one or more semantic errors
    error_type = random.choice(["negative_amount", "future_date", "invalid_currency", "self_transfer"])
    
    if error_type == "negative_amount":
        message["amount"] = round(random.uniform(-1000.0, -1.0), 2)
    elif error_type == "future_date":
        future_date = datetime.now() + timedelta(days=random.randint(30, 365))
        message["settlement_date"] = str(future_date.date())
    elif error_type == "invalid_currency":
        message["currency"] = "XYZ"  # Invalid currency code
    elif error_type == "self_transfer":
        message["receiver_iban"] = message["sender_iban"]
        
    return message

def main():
    print(f"Generating {TOTAL_RECORDS} records...")
    records = []
    
    num_clean = int(TOTAL_RECORDS * CLEAN_RATIO)
    num_corrupt = TOTAL_RECORDS - num_clean
    
    for _ in range(num_clean):
        record = {
            "label": "SAFE",
            "message": generate_clean_message()
        }
        records.append(record)
        
    for _ in range(num_corrupt):
        record = {
            "label": "FLAGGED",
            "message": generate_corrupt_message()
        }
        records.append(record)
        
    # Shuffle records to mix labels
    random.shuffle(records)
    
    with jsonlines.open(OUTPUT_FILE, mode='w') as writer:
        writer.write_all(records)
        
    print(f"Successfully generated {TOTAL_RECORDS} records in {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
