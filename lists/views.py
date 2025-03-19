from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from lists.models import Item, List


def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html",)


def new_list(request: HttpRequest) -> HttpResponse:
    new_list: List = List.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=new_list)
    return redirect("/lists/the-only-list-in-the-world/")


def view_list(request: HttpRequest) -> HttpResponse:
    items = Item.objects.all()
    return render(request, "list.html", {"items": items},)
