import platform
from selenium import webdriver


def get_browser():
    system: str = platform.system()

    if system == "Darwin":
        return webdriver.Safari()
    elif system == "Windows":
        return webdriver.Edge()
    else:
        return webdriver.Firefox()
