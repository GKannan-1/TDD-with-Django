import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from typing import Protocol, cast


class Support(Protocol):
    def get_attribute(self, name: str) -> str | None: ...
    def find_elements(self, by: str, value: str |
                      None = None) -> list[WebElement]: ...


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Safari()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_todo_list(self):
        # Edith has heard about a cool new online to-do app
        # She goes to check out its homepage
        self.browser.get("http://localhost:8000")

        # She notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text: str = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # She is invited to enter a to-do item straight away
        input_box: WebElement = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(cast(Support, input_box).get_attribute(
            "placeholder"), "Enter a to-do item")

        # She types "Buy peacock feathers" into a text box
        # (Edith's hobby is fly-fishing lures)
        input_box.send_keys("Buy peacock feathers")

        # When she hits enter, the page updates, and now the page lists
        # "1. Buy peacock feathers" as an item in a to-do list table
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        table: WebElement = self.browser.find_element(By.ID, "id_list_table")
        rows: list[WebElement] = cast(
            Support, table).find_elements(By.TAG_NAME, "tr")
        self.assertTrue(
            any(row.text == "1. Buy peacock feathers" for row in rows))

        # There is still a textbox inviting her to add another item
        # She enters "Use peacock feathers to make a fly"
        # (Edith is very methodical)
        self.fail("Finish the test!")

        # The page updates again, and now shows both items on her list

        # Satisfied, she goes back to sleep


if __name__ == "__main__":
    unittest.main()
