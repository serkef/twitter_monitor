import json

from tweepy import StreamListener

from config import EXPORT_ROOT
from utilities import get_screenshot


class Listener(StreamListener):
    def on_status(self, status):
        """ on_status callback. Filters out Retweets and comments"""
        print(".", end="", flush=True)

        tweet_path = EXPORT_ROOT / f"{status.id}"
        tweet_path.mkdir(exist_ok=True, parents=True)
        with open(tweet_path / f"{status.id}.json", "a", encoding="utf8") as fout:
            json.dump(status._json, fout, ensure_ascii=False)

        get_screenshot(status.id, tweet_path)

    def on_error(self, status_code):
        print(status_code)
        return False
