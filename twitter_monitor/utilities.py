""" custom utilities """

from pathlib import Path

from selenium import webdriver

from config import BROWSERLESS_TOKEN

def get_screenshot(tweet_id: str, output_directory: Path) -> None:
    """ Gets a screenshot from a tweet """

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    capabilities = chrome_options.to_capabilities()
    if BROWSERLESS_TOKEN:
        capabilities['browserless.token'] = BROWSERLESS_TOKEN

    driver = webdriver.Remote(
        command_executor="https://chrome.browserless.io/webdriver",
        desired_capabilities=chrome_options.to_capabilities(),
    )

    driver.get(f"https://twitter.com/i/web/status/{tweet_id}")
    driver.save_screenshot(str(output_directory / f"{tweet_id}.png"))
    driver.quit()
