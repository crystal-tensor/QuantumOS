import json
import sys
try:
    from jsonschema import validate, ValidationError
except ImportError:
    print("jsonschema module not found. Please install it using 'pip install jsonschema'")
    sys.exit(1)

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def main():
    schema_path = 'docs/spec/api_contract_v1.json'
    
    try:
        schema = load_json(schema_path)
    except Exception as e:
        print(f"Error loading schema: {e}")
        sys.exit(1)

    # Valid Job Request
    valid_request = {
        "job_id": "123e4567-e89b-12d3-a456-426614174000",
        "tenant_id": "user_001",
        "required_qubits": 2,
        "expected_duration_ns": 5000,
        "qisa_instructions": [
            { "opcode": "QALLOC", "operands": [0] },
            { "opcode": "U3", "operands": [0, 1.57, 0.0, 3.14] },
            { "opcode": "WAIT", "operands": [0, 100] },
            { "opcode": "MEASURE", "operands": [0, 0] }
        ]
    }

    try:
        # Note: When validating a sub-schema that has references, we need to pass the full schema as a resolver
        # or construct a validator that knows about the root schema.
        from jsonschema.validators import validator_for
        
        validator_cls = validator_for(schema)
        validator = validator_cls(schema) # Initialize with root schema to resolve #/definitions
        
        # Validate JobRequest
        # We need to find the specific sub-schema but use the root validator
        request_schema = schema["definitions"]["JobRequest"]
        
        # Manually triggering validation with correct context is tricky with simple 'validate'
        # Instead, we can just validate against the root schema since our example matches oneOf JobRequest
        
        validator.validate(valid_request)
        print("Validation Successful: JobRequest conforms to schema.")
    except ValidationError as e:
        print(f"JobRequest Validation Error: {e.message}")
        print(f"Validation context: {e.context}")
        sys.exit(1)

    # Valid Job Response
    valid_response = {
        "job_id": "123e4567-e89b-12d3-a456-426614174000",
        "status": "COMPLETED",
        "results": {
            "00": 0.49,
            "11": 0.51
        },
        "execution_time_ns": 4800
    }

    try:
        validator.validate(valid_response)
        print("Validation Successful: JobResponse conforms to schema.")
        print("M1-API 契约定义完成")
    except ValidationError as e:
        print(f"JobResponse Validation Error: {e.message}")
        sys.exit(1)

if __name__ == "__main__":
    main()
