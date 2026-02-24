import json
from jsonschema import validate, ValidationError
import jsonlines

# Configuration
SCHEMA_FILE = "data_generator/schema.json"
DATASET_FILE = "data_generator/dataset.jsonl"

def load_schema():
    with open(SCHEMA_FILE, 'r') as f:
        return json.load(f)

def validate_dataset():
    schema = load_schema()
    valid_count = 0
    total_count = 0
    
    print(f"Validating dataset against schema: {SCHEMA_FILE}...")
    
    with jsonlines.open(DATASET_FILE) as reader:
        for record in reader:
            total_count += 1
            message = record["message"]
            try:
                validate(instance=message, schema=schema)
                valid_count += 1
            except ValidationError as e:
                print(f"Validation error in record {total_count}: {e.message}")
                
    print(f"Summary: {valid_count}/{total_count} records are syntactically valid.")
    
    if valid_count == total_count:
        print("Dataset is syntactically sound.")
    else:
        print("Dataset contains invalid JSON messages according to schema.")

if __name__ == "__main__":
    validate_dataset()
