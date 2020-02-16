""" custom utilities """

import json
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

import requests
from selenium import webdriver

from config import BROWSERLESS_TOKEN, APP_LOGS


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

    logger = logging.getLogger(f"{__name__}.get_screenshot_api")
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
        logger.error("Can't save screenshot.", exc_info=True)


def set_logging(loglevel: [int, str] = "INFO"):
    """ Sets logging handlers """

    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(fmt)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(loglevel)

    APP_LOGS.mkdir(parents=True, exist_ok=True)
    log_path = f"{APP_LOGS / 'twitter-monitor.log'}"
    file_handler = TimedRotatingFileHandler(
        filename=log_path, when="midnight", encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(loglevel)

    errlog_path = f"{APP_LOGS / 'twitter-monitor.err'}"
    err_file_handler = TimedRotatingFileHandler(
        filename=errlog_path, when="midnight", encoding="utf-8"
    )
    err_file_handler.setFormatter(formatter)
    err_file_handler.setLevel(logging.WARNING)

    logger = logging.getLogger()
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.addHandler(err_file_handler)
    logger.setLevel(loglevel)
