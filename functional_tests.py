from selenium import webdriver

with webdriver.Safari() as browser:
    browser.get("http://localhost:8000")

    assert "Congratulations" in browser.title
    print("OK")
