""" Custom stream listener """

import json
import datetime
import logging
from time import sleep

from tweepy import StreamListener

from .config import EXPORT_ROOT, STORE_SCREENSHOTS
from .utilities import get_screenshot


class Listener(StreamListener):
    def on_status(self, status):
        """ on_status callback. Filters out Retweets and comments"""

        logger = logging.getLogger(f"{__name__}.Listener.on_status")
        logger.info(f"status: {status.id}", extra=status._json)

        date_str = f"{datetime.date.today().isoformat()}"
        tweet_path = EXPORT_ROOT / date_str / f"{status.id}"
        tweet_path.mkdir(exist_ok=True, parents=True)
        with open(tweet_path / f"{status.id}.json", "a", encoding="utf8") as fout:
            json.dump(status._json, fout, ensure_ascii=False)

        if STORE_SCREENSHOTS:
            get_screenshot(status.id, tweet_path)

    def on_error(self, status_code):
        """ on_error callback. Works to handle exceptions"""

        logger = logging.getLogger(f"{__name__}.Listener.on_error")
        logger.error(f"Got error: {status_code}")
        if status_code in {406, 420}:
            logger.info("Sleeping...")
            sleep(60)

        return False
