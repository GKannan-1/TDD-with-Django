from django.db.models.manager import BaseManager
from django.test import TestCase
from django.http import HttpResponse
from lists.models import Item, List


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response: HttpResponse = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response: HttpResponse = self.client.get(
            "/lists/the-only-list-in-the-world/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_all_list_items(self):
        my_list: List = List.objects.create()
        Item.objects.create(text="itemey 1", list=my_list)
        Item.objects.create(text="itemey 2", list=my_list)
        response: HttpResponse = self.client.get(
            "/lists/the-only-list-in-the-world/")
        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        # Using index instead of first() as first() can return None if the Item.objects is empty, but we are already checking if it's empty
        new_item: Item = Item.objects.all()[0]
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response: HttpResponse = self.client.post(
            "/lists/new", data={"item_text": "A new list item"})
        self.assertRedirects(response, "/lists/the-only-list-in-the-world/")


class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        my_list = List()
        my_list.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = my_list
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = my_list
        second_item.save()

        saved_list = List.objects.get()
        self.assertEqual(saved_list, my_list)

        saved_items: BaseManager[Item] = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item: Item = saved_items[0]
        second_saved_item: Item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item",)
        self.assertEqual(first_saved_item.list, my_list)
        self.assertEqual(second_saved_item.text, "Item the second",)
        self.assertEqual(second_saved_item.list, my_list)
