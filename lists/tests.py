from django.test import TestCase
from django.http import HttpResponse


class HomePageTest(TestCase):
    def test_home_page_correct_html(self):
        response: HttpResponse = self.client.get("/")
        self.assertContains(response, "<title>To-Do lists<title>")
        self.assertContains(response, "<html>")
        self.assertContains(response, "</html>")

    def test_home_page_returns_correct_html_2(self):
        response: HttpResponse = self.client.get("/")
        self.assertContains(response, "<title>To-Do lists<title>")
