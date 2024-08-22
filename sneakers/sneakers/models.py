from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Модели для работы с корзиной и заказами


# Модели для работы с кроссовками
class SneakerColor(models.Model):
    color_code = models.CharField(max_length=7, unique=True)
    color_name = models.CharField(max_length=50)

    def __str__(self):
        return self.color_name


class SneakerBrand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to="brand_logos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Sneaker(models.Model):
    brand = models.ForeignKey(
        SneakerBrand, on_delete=models.CASCADE, verbose_name="Бренд"
    )
    model = models.CharField(max_length=100, verbose_name="Модель")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    size = models.DecimalField(max_digits=4, decimal_places=1, verbose_name="Размер")
    color = models.ForeignKey(
        SneakerColor, on_delete=models.CASCADE, verbose_name="Цвет"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(
        upload_to="sneakers/", verbose_name="Изображение", blank=True, null=True
    )
    stock = models.PositiveIntegerField(verbose_name="В наличии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Создатель"
    )

    def __str__(self):
        return f"{self.brand.name} {self.model} ({self.size})"

    class Meta:
        verbose_name = "Кроссовок"
        verbose_name_plural = "Кроссовки"
        ordering = ["brand", "model"]

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username} created at {self.created_at}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    sneaker = models.ForeignKey(Sneaker, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.sneaker} x {self.quantity} in cart for {self.cart.user.username}"


class SneakerLike(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    sneaker = models.ForeignKey(
        Sneaker, on_delete=models.CASCADE, verbose_name="Кроссовок"
    )
    liked_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата добавления в избранное"
    )

    def __str__(self):
        return f"{self.user.username} likes {self.sneaker}"

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"
        unique_together = ("user", "sneaker")


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "В ожидании"),
            ("Shipped", "Отправлен"),
            ("Delivered", "Доставлен"),
        ],
        default="Pending",
    )

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    sneaker = models.ForeignKey("Sneaker", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.sneaker} for Order #{self.order.id}"

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    sneaker = models.ForeignKey(Sneaker, on_delete=models.CASCADE, verbose_name="Кроссовок")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        unique_together = ('user', 'sneaker')  # Убедитесь, что один пользователь не может добавить один и тот же кроссовок дважды
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные кроссовки"

    def __str__(self):
        return f"{self.user.username} - {self.sneaker.model}"