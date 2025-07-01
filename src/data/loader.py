import json

def load_instance(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data
