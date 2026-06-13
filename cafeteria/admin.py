from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Product, Dish, Menu, Order, PurchaseRequest, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль'
    fields = ('role',)

class CustomUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')

    @admin.display(description='Роль')
    def get_role(self, obj):
        try:
            return obj.profile.get_role_display()
        except Profile.DoesNotExist:
            return "Нет профиля"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # если профиль еще не создан , создаем его
        if not hasattr(obj, 'profile'):
            Profile.objects.create(user=obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'unit')
    search_fields = ('name',)
    list_filter = ('unit',)

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'dish_type', 'price')
    list_filter = ('dish_type',)
    search_fields = ('name',)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('date', 'dish', 'portions_available')
    list_filter = ('date', 'dish__dish_type')
    date_hierarchy = 'date'
    search_fields = ('dish__name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'menu_item', 'issued_at', 'is_issued')
    list_filter = ('is_issued', 'issued_at', 'menu_item__dish__dish_type')
    search_fields = ('student__username', 'menu_item__dish__name')
    date_hierarchy = 'issued_at'
    readonly_fields = ('issued_at',)

@admin.register(PurchaseRequest)
class PurchaseRequestAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_needed', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('product__name', 'created_by__username')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)