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
        my_list: List = List.objects.create()
        response: HttpResponse = self.client.get(
            f"/lists/{my_list.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_all_list_items(self):
        correct_list: List = List.objects.create()
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)

        other_list: List = List.objects.create()
        Item.objects.create(text="other list item", list=other_list)

        response: HttpResponse = self.client.get(
            f"/lists/{correct_list.id}/")

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, "other list item")

    def test_passes_correct_list_to_template(self):
        # other_list created to ensure response is sending out the right list and not just the only list
        other_list: List = List.objects.create()  # type: ignore
        correct_list: List = List.objects.create()
        response: HttpResponse = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"], correct_list)


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
        new_list: List = List.objects.get()
        self.assertRedirects(response, f"/lists/{new_list.id}/")


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        # Same reason as previous type ignore
        other_list: List = List.objects.create()  # type: ignore
        correct_list: List = List.objects.create()

        self.client.post(f"/lists/{correct_list.id}/add_item",
                         data={"item_text": "A new item for an existing list"},)

        self.assertEqual(Item.objects.count(), 1)
        new_item: Item = Item.objects.get()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        # again, same reason as previous (and previous) type ignore
        other_list: List = List.objects.create()  # type: ignore
        correct_list: List = List.objects.create()

        response: HttpResponse = self.client.post(
            f"/lists/{correct_list.id}/add_item", data={"item_text": "A new item for an existing list"},)

        self.assertRedirects(response, f"/lists/{correct_list.id}/")


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
