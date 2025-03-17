import platform
from selenium import webdriver


def get_browser():
    system: str = platform.system()

    if system == "Darwin":
        return webdriver.Safari()
    else:
        return webdriver.Firefox()
