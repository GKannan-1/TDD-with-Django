from django.db.models.manager import BaseManager
from django.test import TestCase
from django.http import HttpResponse
from lists.models import Item


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response: HttpResponse = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_can_save_a_POST_request(self):
        response: HttpResponse = self.client.post(
            "/", data={"item_text": "A new list item"})
        self.assertContains(response, "A new list item")
        self.assertTemplateUsed(response, "home.html")


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.save()

        saved_items: BaseManager[Item] = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item: Item = saved_items[0]
        second_saved_item: Item = saved_items[1]
        self.assertEqual("The first (ever) list item", first_saved_item.text)
        self.assertEqual("Item the second", second_saved_item.text)
