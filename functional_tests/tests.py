import time
from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import WebDriverException
from typing import Protocol, cast
from browser import get_browser

MAX_WAIT = 5


class Support(Protocol):
    def get_attribute(self, name: str) -> str | None: ...
    def find_elements(self, by: str, value: str |
                      None = None) -> list[WebElement]: ...


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = get_browser()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text: str, contains: bool = True):
        """This helper method is case sensitive, write the entire excepted or unexpected string"""
        start_time: float = time.time()
        while True:
            try:
                table: WebElement = self.browser.find_element(
                    By.ID, "id_list_table")
                rows: list[WebElement] = cast(
                    Support, table).find_elements(By.TAG_NAME, "tr")

                if contains:
                    self.assertIn(row_text, [row.text for row in rows],)
                else:
                    self.assertNotIn(row_text, [row.text for row in rows],)
                return
            except (WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)

    def test_can_start_a_todo_list(self):
        # Edith has heard about a cool new online to-do app
        # She goes to check out its homepage
        self.browser.get(self.live_server_url)

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
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # There is still a textbox inviting her to add another item
        # She enters "Use peacock feathers to make a fly"
        # (Edith is very methodical)
        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("Use peacock feathers to make a fly")
        input_box.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table(
            "2: Use peacock feathers to make a fly")

        # Satisfied, she goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        input_box: WebElement = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("Buy peacock feathers")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # She notices that her list has a unique URL
        edith_list_url: str = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")

        # Now a new user, Francis, comes along to the site

        # We delete all the browser's cookies
        # as a way of simulating a brand new user session
        self.browser.delete_all_cookies()

        # Francis visits the home page.
        self.browser.get(self.live_server_url)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith... There is no sign of
        # Edith's List
        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("Buy milk")
        input_box.send_keys(Keys.ENTER)
        # Technically only need to check for Buy milk because if buy peacock feathers existed, buy milk would be number 2. However, with this error
        # It lets us know that Buy peacock feathers was saved as number 1, meaning it lets us know that the data was saved after reloading the cookies
        # And not that the data was corrupted or the browser didn't load properly and the like.
        self.wait_for_row_in_list_table("1: Buy peacock feathers", False)
        self.wait_for_row_in_list_table("1: Buy milk")

        # Francis gets his own unique URL
        francis_list_url: str = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)

        # Satisfied, they both go back to sleep
