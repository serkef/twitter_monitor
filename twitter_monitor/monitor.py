""" Monitoring entrypoint """

from typing import List, Any

import tweepy
from tweepy.streaming import Stream
from urllib3.exceptions import ReadTimeoutError

from common import api
from config import RESOURCES
from listener import Listener


def get_following_users() -> List[Any]:
    """ Reads `follow-user.txt` from resources, gets user id from handler """

    users = []
    print("Populating list with users to follow", flush=True)
    with open(RESOURCES / 'follow-user.txt', 'r') as fin:
        for handler in fin.readlines():
            try:
                users.append(str(api.get_user(screen_name=handler).id))
            except tweepy.error.TweepError:
                continue

    return users


def get_following_searches() -> List[Any]:
    """ Reads `follow-search.txt` from resources """

    with open(RESOURCES / 'follow-search.txt', 'r') as fin:
        return [s for s in fin.readlines() if s]


def main():
    """ Main run function """

    following = get_following_users()
    tracks = get_following_searches()

    print(f"Following {len(following)} users and {len(tracks)} searches")
    while True:
        listener = Listener()
        stream = Stream(auth=api.auth, listener=listener)
        try:
            print("Started streaming", flush=True)
            stream.filter(follow=following, track=tracks)
        except KeyboardInterrupt as e:
            print("Stopped.")
            break
        except ReadTimeoutError as e:
            print("Handled exception:", str(e))
        finally:
            print("Done.")
            stream.disconnect()


if __name__ == '__main__':
    main()
