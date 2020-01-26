""" custom utilities """
import json
from pathlib import Path

import requests
from selenium import webdriver

from config import BROWSERLESS_TOKEN


def get_screenshot(*args, **kwargs) -> None:
    """ Gets a screenshot from a tweet """

    get_screenshot_api(*args, **kwargs)


def get_screenshot_selenium(tweet_id: str, output_directory: Path) -> None:
    """ Takes a screenshot using selenium with browserless engine """

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    capabilities = chrome_options.to_capabilities()
    if BROWSERLESS_TOKEN:
        capabilities["browserless.token"] = BROWSERLESS_TOKEN

    driver = webdriver.Remote(
        command_executor="https://chrome.browserless.io/webdriver",
        desired_capabilities=chrome_options.to_capabilities(),
    )
    try:
        driver.get(f"https://twitter.com/i/web/status/{tweet_id}")
        driver.save_screenshot(str(output_directory / f"{tweet_id}.png"))
    finally:
        driver.quit()


def get_screenshot_api(tweet_id: str, output_directory: Path) -> None:
    """ Takes a screenshot calling the browserless screenshot API """

    api_url = f"https://chrome.browserless.io/screenshot"
    params = {"token": BROWSERLESS_TOKEN}
    headers = {"Cache-Control": "no-cache", "Content-Type": "application/json"}
    payload = {
        "url": f"https://twitter.com/i/web/status/{tweet_id}",
        "options": {"fullPage": True, "type": "jpeg", "quality": 5},
    }
    response = requests.post(
        api_url, headers=headers, params=params, data=json.dumps(payload)
    )
    try:
        response.raise_for_status()
        with open(output_directory / f"{tweet_id}.jpg", "wb") as fout:
            fout.write(response.content)
    except Exception as exc:
        print("Can't save screenshot.", exc)
