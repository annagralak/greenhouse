import json

def load_config(path):
    """Load JSON config file; return dict or None on failure."""
    
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load config {path}: {e}")
        return None

def pretty_print(data, indent=0, is_root=True):
    if is_root:
        print("-" * 60)

    prefix = "    " * indent

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                print(f"{prefix}{key}:")
                pretty_print(value, indent + 1, False)
            else:
                print(f"{prefix}{key}: {value}")
 
    elif isinstance(data, list):
        for i, item in enumerate(data):
            print(f"{prefix}- [{i}]")
            pretty_print(item, indent + 1, False)
    else:
        print(f"{prefix}{data}")
