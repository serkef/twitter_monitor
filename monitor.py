import os
from base64 import b64decode
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import tweepy
import requests
from tweepy.streaming import StreamListener, Stream, json
from urllib3.exceptions import ReadTimeoutError


class Listener(StreamListener):
    def __init__(self, output_file='twitter_monitor.json', posted_by=None):
        super(Listener, self).__init__()
        self.posted_by = posted_by or set()
        self.output_file = output_file

    def on_status(self, status):
        # Filter out RTs and comments
        # if self.posted_by and status.author.screen_name not in self.posted_by \
        #         or "retweeted_status" in status._json:
        #     return
        print('.', end='', flush=True)
        with open(self.output_file, 'a', encoding='utf8') as fout:
            json.dump(status._json, fout, ensure_ascii=False)

        self.get_screenshot(status.id)

    def on_error(self, status_code):
        print(status_code)
        return False

    def get_screenshot(self, tweet_id):

        # url = ("https://www.googleapis.com/pagespeedonline/v1/runPagespeed?"
        #    "screenshot=true&url="
        #    "https://twitter.com/i/web/status/{id}").format(id=tweet_id)
        # shot_file = f"{tweet_id}.jpg"
        # try:
        #     shot = requests.get(url).json()['screenshot']['data']
        #     data = b64decode(shot.replace("_", "/").replace("-", "+"))
        # except Exception:
        #     return
        #
        # with open(shot_file, 'wb') as jpg:
        #     jpg.write(data)
        # return shot_file
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")

        driver = webdriver.Remote(
            command_executor='https://chrome.browserless.io/webdriver',
            desired_capabilities=chrome_options.to_capabilities()
        )

        driver.get(f"https://twitter.com/i/web/status/{tweet_id}")
        driver.save_screenshot(f'{tweet_id}.png')
        driver.quit()


auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_KEY_SECRET'))
auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
following = [u for u in
             tweepy.Cursor(api.list_members, owner_screen_name='serkef', slug='p01').items(1000)]

while True:
    listener = Listener(posted_by=set(u.screen_name for u in following))
    stream = Stream(auth=api.auth, listener=listener)
    try:
        print('Started streaming')
        stream.filter(follow=[str(u.id) for u in following])
    except KeyboardInterrupt as e:
        print("Stopped.")
        break
    except ReadTimeoutError as e:
        print("Handled exception:", str(e))
    finally:
        print('Done.')
        stream.disconnect()
