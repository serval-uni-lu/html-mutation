import contextlib

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--incognito")
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging"]
    )
    
    return webdriver.Chrome(options=chrome_options)
