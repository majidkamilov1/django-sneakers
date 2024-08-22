from atexit import register
from django.urls import path
from .views import (
    ChangeUserDataView,
    LoginView,
    LogoutView,
    ProfileView,
    RegisterView,
    add_to_cart,
    favorite_list,
    index,
    remove_from_cart,
    remove_from_favorites,
    toggle_cart_item,
    toggle_favorite,
    update_cart_item_quantity,
    view_cart,
)

urlpatterns = [
    path("", index, name="home"),
    path('register/', RegisterView.as_view(), name='register'),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/change", ChangeUserDataView.as_view(), name="change-user-data"),
    path("cart/", view_cart, name="view_cart"),
    path("cart/add/<int:sneaker_id>/", add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", remove_from_cart, name="remove_from_cart"),
    path("cart/toggle/<int:sneaker_id>/", toggle_cart_item, name="toggle_from_cart"),
    path(
        "cart/update/<int:cart_item_id>/<str:action>/",
        update_cart_item_quantity,
        name="update_cart_item_quantity",
    ),
    path("favorites/", favorite_list, name="favorite_list"),
    path("favorites/toggle/<int:sneaker_id>/", toggle_favorite, name="toggle_favorite"),
    path(
        "favorites/remove/<int:sneaker_id>/",
        remove_from_favorites,
        name="remove_favorite",
    ),
]
