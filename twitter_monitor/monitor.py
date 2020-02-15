""" Monitoring entrypoint """

import os
from typing import List, Any

import tweepy
from tweepy import API
from tweepy.streaming import Stream
from urllib3.exceptions import ReadTimeoutError

from config import TWITTER_FOLLOW_SEARCHES_FILE, TWITTER_FOLLOW_USERS_FILE
from listener import Listener


def get_following_users(api: API) -> List[Any]:
    """ Reads file with users as defined in TWITTER_FOLLOW_USERS_FILE """

    users = []
    if not TWITTER_FOLLOW_USERS_FILE:
        return users
    with open(TWITTER_FOLLOW_USERS_FILE) as fin:
        for handler in fin.readlines():
            try:
                users.append(str(api.get_user(screen_name=handler).id))
            except tweepy.error.TweepError:
                continue

    return users


def get_default_users(api: API) -> List[Any]:
    """ Returns default list of users to follow from a custom list """

    return [
        str(u.id)
        for u in tweepy.Cursor(
            api.list_members, owner_screen_name="serkef", slug="p01"
        ).items(1000)
    ]


def get_following_searches() -> List[Any]:
    """ Reads file with searches as defined in TWITTER_FOLLOW_SEARCHES_FILE """

    if not TWITTER_FOLLOW_SEARCHES_FILE:
        return []
    with open(TWITTER_FOLLOW_SEARCHES_FILE, "r") as fin:
        return [s for s in fin.readlines() if s]


def main():
    """ Main run function """

    auth = tweepy.OAuthHandler(
        os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_KEY_SECRET")
    )
    auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    following = get_following_users(api)
    following.extend(get_default_users(api))
    tracks = get_following_searches()

    print(f"Following {len(following)} users and {len(tracks)} searches")
    while True:
        listener = Listener()
        stream = Stream(auth=api.auth, listener=listener)
        try:
            print("Started streaming", flush=True)
            stream.filter(follow=following, track=tracks)
        except KeyboardInterrupt:
            print("Stopped")
            break
        except ReadTimeoutError as exc:
            print("Handled exception:", str(exc))
        finally:
            print("Done")
            stream.disconnect()


if __name__ == "__main__":
    main()
