from django.test import TestCase
from django.http import HttpRequest, HttpResponse
from .views import home_page


class HomePageTest(TestCase):
    def test_home_page_correct_html(self):
        request = HttpRequest()
        response: HttpResponse = home_page(request)
        html: str = response.content.decode("utf8")
        self.assertIn("<title>To-Do lists<title>", html)
        self.assertTrue(html.startswith("<html>"))
        self.assertTrue(html.endswith("<html>"))
