from pathlib import Path

DB_DIR = Path('data')
METADATA_FILE = DB_DIR / 'metadata.json'

TYPE_MAP = {'int': int, 'str': str, 'bool': bool}
