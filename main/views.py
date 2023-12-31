from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from main.forms import WeaponForm
from main.models import Weapons
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json


@login_required(login_url="/login")
def show_main(request):
    weapons = Weapons.objects.filter(user=request.user)
    counter = weapons.count()
    context = {
        "name": request.user.username,
        "weapons": weapons,
        "counter": counter,
        "class": "International Class",
        "last_login": request.COOKIES["last_login"]
        if "last_login" in request.COOKIES.keys()
        else "",
    }

    return render(request, "main.html", context)


def create_weapon(request):
    form = WeaponForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        weapon = form.save(commit=False)
        weapon.user = request.user
        weapon.save()
        return HttpResponseRedirect(reverse("main:show_main"))

    context = {"form": form}
    return render(request, "create_weapon.html", context)


def show_xml(request):
    data = Weapons.objects.all()
    return HttpResponse(
        serializers.serialize("xml", data), content_type="application/xml"
    )


def show_json(request):
    data = Weapons.objects.all()
    return HttpResponse(
        serializers.serialize("json", data), content_type="application/json"
    )


def show_xml_by_id(request, id):
    data = Weapons.objects.filter(pk=id)
    return HttpResponse(
        serializers.serialize("xml", data), content_type="application/xml"
    )


def show_json_by_id(request, id):
    data = Weapons.objects.filter(pk=id)
    return HttpResponse(
        serializers.serialize("json", data), content_type="application/json"
    )


def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been successfully created!")
            return redirect("main:login")
    context = {"form": form}
    return render(request, "register.html", context)


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie("last_login", str(datetime.datetime.now()))
            return response
        else:
            messages.info(
                request, "Sorry, incorrect username or password. Please try again."
            )
    context = {}
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse("main:login"))
    response.delete_cookie("last_login")
    return response


def increment(request, id):
    weapon = Weapons.objects.get(pk=id)
    weapon.amount += 1
    weapon.save()
    return HttpResponseRedirect(reverse("main:show_main"))


def decrement(request, id):
    weapon = Weapons.objects.get(pk=id)
    if weapon.amount > 0:
        weapon.amount -= 1
        weapon.save()
    return HttpResponseRedirect(reverse("main:show_main"))


def delete(request, id):
    weapon = Weapons.objects.get(pk=id)
    weapon.delete()
    return HttpResponseRedirect(reverse("main:show_main"))


def edit_product(request, id):
    product = Weapons.objects.get(pk=id)
    form = WeaponForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse("main:show_main"))
    context = {"form": form}
    return render(request, "edit_product.html", context)


def get_product_json(request):
    weapons = Weapons.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", weapons))


@csrf_exempt
def add_product_ajax(request):
    if request.method == "POST":
        name = request.POST.get("name")
        type = request.POST.get("type")
        attack_rating = request.POST.get("attack_rating")
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        user = request.user

        new_product = Weapons(
            name=name,
            type=type,
            attack_rating=attack_rating,
            amount=amount,
            description=description,
            user=user,
        )
        new_product.save()
        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()


@csrf_exempt
def delete_product_ajax(request, id):
    product = Weapons.objects.get(pk=id)
    product.delete()
    return HttpResponse(b"DELETED", status=201)


@csrf_exempt
def create_product_flutter(request):
    if request.method == "POST":
        data = json.loads(request.body)

        new_product = Weapons.objects.create(
            user=request.user,
            name=data["name"],
            price=int(data["price"]),
            description=data["description"],
        )

        new_product.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
