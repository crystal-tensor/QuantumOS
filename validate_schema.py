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
    schema_path = 'docs/spec/device_spec_v0.json'
    
    try:
        schema = load_json(schema_path)
    except FileNotFoundError:
        print(f"Error: Schema file not found at {schema_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in schema file: {e}")
        sys.exit(1)

    # Example valid device specification
    valid_device = {
        "schema_version": "v1.0",
        "qpu_id": "qos_qpu_001",
        "description": "5-qubit star topology processor with high coherence times.",
        "qubit_count": 5,
        "qubits": [
            {
                "id": 0,
                "t1_us": 50.5,
                "t2_us": 70.2,
                "frequency_ghz": 4.5,
                "readout_fidelity": 0.98
            },
            {
                "id": 1,
                "t1_us": 48.0,
                "t2_us": 65.0,
                "frequency_ghz": 4.6,
                "readout_fidelity": 0.97
            },
             {
                "id": 2,
                "t1_us": 52.0,
                "t2_us": 68.0,
                "frequency_ghz": 4.55,
                "readout_fidelity": 0.985
            },
             {
                "id": 3,
                "t1_us": 49.5,
                "t2_us": 66.5,
                "frequency_ghz": 4.48,
                "readout_fidelity": 0.975
            },
             {
                "id": 4,
                "t1_us": 51.0,
                "t2_us": 69.0,
                "frequency_ghz": 4.62,
                "readout_fidelity": 0.98
            }
        ],
        "coupling_map": [
            [0, 1], [1, 0],
            [0, 2], [2, 0],
            [0, 3], [3, 0],
            [0, 4], [4, 0]
        ],
        "gate_set": {
            "single_qubit": [
                {"name": "U3", "duration_ns": 20, "avg_fidelity": 0.999},
                {"name": "X", "duration_ns": 20, "avg_fidelity": 0.999},
                 {"name": "H", "duration_ns": 20, "avg_fidelity": 0.999}
            ],
            "two_qubit": [
                {"name": "CX", "duration_ns": 50, "avg_fidelity": 0.995}
            ]
        }
    }

    try:
        validate(instance=valid_device, schema=schema)
        print("Validation Successful: The sample device specification conforms to the schema.")
        print("M1-Spec 规范初始化完成")
    except ValidationError as e:
        print(f"Validation Error: {e.message}")
        sys.exit(1)

if __name__ == "__main__":
    main()
