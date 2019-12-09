import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# Screenshots
STORE_SCREENSHOTS = True

# Export location
EXPORT_ROOT = Path(os.getenv('EXPORT_ROOT'))
