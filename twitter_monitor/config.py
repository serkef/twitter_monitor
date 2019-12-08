import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# Screenshots
STORE_SCREENSHOTS = True

# Export location
EXPORT_ROOT = os.getenv('EXPORT_ROOT')
