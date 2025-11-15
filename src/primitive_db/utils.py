import json


def load_metadata(filepath):
    try:
        with open(filepath) as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    with open(filepath, 'w') as f:
        f.write(json.dumps(data, indent=2))
