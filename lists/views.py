from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from lists.models import Item, List
from django.db.models import AutoField


def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html",)


def new_list(request: HttpRequest) -> HttpResponse:
    new_list: List = List.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=new_list)
    return redirect(f"/lists/{new_list.id}/")


def view_list(request: HttpRequest, list_id: AutoField) -> HttpResponse:
    our_list: List = List.objects.get(id=list_id)
    return render(request, "list.html", {"list": our_list},)


def add_item(request: HttpRequest, list_id: AutoField) -> HttpResponse:
    our_list: List = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["item_text"], list=our_list)
    return redirect(f"/lists/{our_list.id}/")
