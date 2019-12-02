import os

import tweepy
from tweepy.streaming import StreamListener, Stream, json
from urllib3.exceptions import ReadTimeoutError

from config import EXPORT_ROOT
from utilities import get_screenshot


class Listener(StreamListener):
    def __init__(self, posted_by=None):
        super(Listener, self).__init__()
        self.posted_by = posted_by or set()

    def on_status(self, status):
        """ on_status callback. Filters out Retweets and comments"""

        # Filter out RTs and comments
        if (
            self.posted_by
            and status.author.screen_name not in self.posted_by
            or "retweeted_status" in status._json
        ):
            return

        print(".", end="", flush=True)

        tweet_path = EXPORT_ROOT / f"{status.id}"
        tweet_path.mkdir(exist_ok=True, parents=True)
        with open(tweet_path / f"{status.id}.json", "a", encoding="utf8") as fout:
            json.dump(status._json, fout, ensure_ascii=False)

        get_screenshot(status.id, tweet_path)

    def on_error(self, status_code):
        print(status_code)
        return False


auth = tweepy.OAuthHandler(os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_KEY_SECRET"))
auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
following = [
    u
    for u in tweepy.Cursor(
        api.list_members, owner_screen_name="serkef", slug="p01"
    ).items(1000)
]

while True:
    listener = Listener(posted_by=set(u.screen_name for u in following))
    stream = Stream(auth=api.auth, listener=listener)
    try:
        print("Started streaming")
        stream.filter(follow=[str(u.id) for u in following])
    except KeyboardInterrupt as e:
        print("Stopped.")
        break
    except ReadTimeoutError as e:
        print("Handled exception:", str(e))
    finally:
        print("Done.")
        stream.disconnect()
