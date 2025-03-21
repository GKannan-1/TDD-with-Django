from django.db.models.manager import BaseManager
from django.test import TestCase
from django.http import HttpResponse
from lists.models import Item


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response: HttpResponse = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_displays_all_list_items(self):
        Item.objects.create(text="itemey 1")
        Item.objects.create(text="itemey 2")
        response: HttpResponse = self.client.get("/")
        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")

    def test_can_save_a_POST_request(self):
        self.client.post("/", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        # Using index instead of first() as first() can return None if the Item.objects is empty, but we are already checking if it's empty
        new_item: Item = Item.objects.all()[0]
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response: HttpResponse = self.client.post(
            "/", data={"item_text": "A new list item"})
        self.assertRedirects(response, "/")

    def test_only_saves_items_when_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)


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
