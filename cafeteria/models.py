from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название продукта")
    quantity = models.FloatField(default=0, verbose_name="Остаток на складе")
    unit = models.CharField(max_length=20, default="кг", verbose_name="Ед. измерения")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

class Dish(models.Model):
    TYPE_CHOICES = [
        ('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('snack', 'Перекус'),
        ('drink', 'Напиток'),
    ]
    name = models.CharField(max_length=100, verbose_name="Название блюда")
    dish_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Тип приема пищи")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Цена")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"

class Menu(models.Model):
    date = models.DateField(verbose_name="Дата")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name="Блюдо")
    portions_available = models.IntegerField(default=0, verbose_name="Доступно порций")

    def __str__(self):
        return f"{self.date} - {self.dish.name}"

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Меню на день"

class Order(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Ученик")
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name="Блюдо из меню")
    issued_at = models.DateTimeField(auto_now_add=True, verbose_name="Время выдачи")
    is_issued = models.BooleanField(default=False, verbose_name="Выдано")

    def __str__(self):
        return f"Заказ {self.id} от {self.student.username}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class PurchaseRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На согласовании'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    quantity_needed = models.FloatField(verbose_name="Требуемое количество")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Кто создал")

    def __str__(self):
        return f"Заявка на {self.product.name} ({self.quantity_needed})"

    class Meta:
        verbose_name = "Заявка на закупку"
        verbose_name_plural = "Заявки на закупки"

class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Ученик'),
        ('cook', 'Повар'),
        ('admin_staff', 'Администратор столовой'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', verbose_name="Роль")

    def __str__(self):
        return f"Профиль {self.user.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

