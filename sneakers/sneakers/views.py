import json
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, UserProfileForm
from .models import Sneaker, Cart, CartItem, Favorite
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User


def index(request):
    query = request.GET.get("q")
    sneakers = Sneaker.objects.all()

    if query:
        sneakers = sneakers.filter(Q(description__icontains=query))

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        cart_sneaker_ids = cart_items.values_list("sneaker_id", flat=True)

        # Получаем избранные кроссовки для текущего пользователя
        favorite_sneakers = Favorite.objects.filter(user=request.user).values_list('sneaker_id', flat=True)
    else:
        cart_items = []
        cart_sneaker_ids = []
        favorite_sneakers = []

    return render(
        request,
        "index.html",
        {
            "sneakers": sneakers,
            "cart_items": cart_items,
            "cart_sneaker_ids": cart_sneaker_ids,
            "favorite_sneakers": favorite_sneakers,  # Добавляем избранные кроссовки в контекст
        },
    )


class ProfileView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        form = UserProfileForm(instance=user)
        return render(request, "auth/profile.html", {"form": form})


class ChangeUserDataView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = UserProfileForm(instance=request.user)
        return render(request, "auth/change-data.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
        return render(request, "auth/change-data.html", {"form": form})


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, "auth/login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")  # Изменено на 'home'
        return render(request, "auth/login.html", {"form": form})

class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'auth/registration.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("home")


@login_required(login_url="login")
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = None

    if cart:
        items = cart.items.all()
        total_price = sum(item.sneaker.price * item.quantity for item in items)
    else:
        items = []
        total_price = 0

    return render(request, "cart.html", {"items": items, "total_price": total_price})


@login_required(login_url="login")  # Укажите URL страницы логина
def add_to_cart(request, sneaker_id):
    if request.method == "POST":
        sneaker = get_object_or_404(Sneaker, id=sneaker_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, sneaker_id=sneaker_id)
        print(item)
        if not created:
            item.quantity += 1
            item.save()
    return redirect("home")


@login_required(login_url="login")
def remove_from_cart(request, item_id):
    CartItem.objects.filter(id=item_id).delete()
    return redirect("view_cart")


@login_required(login_url="login")
def toggle_cart_item(request, sneaker_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, sneaker_id=sneaker_id)

    if created:
        # Товар был добавлен в корзину
        item.quantity = 1
        item.save()
    else:
        # Товар уже есть в корзине, удаляем его
        item.delete()

    return redirect("home")  # Перенаправление на главную страницу


@login_required(login_url="login")
def update_cart_item_quantity(request, cart_item_id, action):
    cart_item = CartItem.objects.get(id=cart_item_id)

    if action == "increase":
        cart_item.quantity += 1
    elif action == "decrease" and cart_item.quantity > 1:
        cart_item.quantity -= 1
    else:
        # Удаление элемента, если количество становится 0
        cart_item.delete()

    cart_item.save()
    return redirect("view_cart")


@login_required
def favorite_list(request):
    favorite_sneakers = Sneaker.objects.filter(favorite__user=request.user)

    return render(
        request,
        "favorites.html",
        {
            "favorite_sneakers": favorite_sneakers,
        }
    )



@login_required(login_url="login")  # Укажите URL страницы логина
def add_to_favorites(request, sneaker_id):
    sneaker = get_object_or_404(Sneaker, id=sneaker_id)
    Favorite.objects.get_or_create(user=request.user, sneaker=sneaker)
    return redirect("home")


@login_required(login_url="login")  # Укажите URL страницы логина
def remove_from_favorites(request, sneaker_id):
    sneaker = get_object_or_404(Sneaker, id=sneaker_id)
    favorite = Favorite.objects.filter(user=request.user, sneaker=sneaker).first()
    if favorite:
        favorite.delete()
    return redirect("favorite_list")

@login_required(login_url="login")  # Укажите URL страницы логина
def toggle_favorite(request, sneaker_id):
    sneaker = get_object_or_404(Sneaker, id=sneaker_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, sneaker=sneaker)

    if not created:
        favorite.delete()  # Если избранное уже существует, удалите его
    return redirect('home')