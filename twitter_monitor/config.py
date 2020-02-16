""" Main configuration and settings """

import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# Screenshots
STORE_SCREENSHOTS = os.getenv("STORE_SCREENSHOTS", "False") == "True"
BROWSERLESS_TOKEN = os.getenv("BROWSERLESS_TOKEN")
TWITTER_FOLLOW_SEARCHES_FILE = os.getenv("TWITTER_FOLLOW_SEARCHES_FILE")
TWITTER_FOLLOW_USERS_FILE = os.getenv("TWITTER_FOLLOW_USERS_FILE")

# Export location
EXPORT_ROOT = Path(os.getenv("EXPORT_ROOT"))

# Log settings
APP_LOGS = Path(os.environ["APP_LOGS"])
APP_LOGLEVEL = os.getenv("APP_LOGLEVEL", "INFO")

# ZeroMQ port
QUEUE_PORT = os.getenv("QUEUE_PORT", "5555")
RESOURCES = Path(__file__).parent / "resources"
