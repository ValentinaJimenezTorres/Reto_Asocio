import json

def load_instance(path):
    """
    Carga un archivo JSON con los datos del problema.
    """
    with open(path, 'r') as f:
        data = json.load(f)
    return data
