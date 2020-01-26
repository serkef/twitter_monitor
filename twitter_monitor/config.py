""" Main configuration and settings """

import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# Screenshots
STORE_SCREENSHOTS = os.getenv("STORE_SCREENSHOTS", "True") == "True"
BROWSERLESS_TOKEN = os.getenv("BROWSERLESS_TOKEN")

# Export location
EXPORT_ROOT = Path(os.getenv("EXPORT_ROOT"))

RESOURCES = Path(__file__).parent / "resources"
