from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from lists.models import Item


def home_page(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"])
        return redirect("/")

    items = Item.objects.all()
    return render(request, "home.html", {"items": items},)
