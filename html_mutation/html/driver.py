from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import contextlib

@contextlib.contextmanager
def chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-default-browser-check')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-default-apps')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_driver = webdriver.Chrome(options=chrome_options)
    try:
        yield chrome_driver
    finally:
        chrome_driver.close()