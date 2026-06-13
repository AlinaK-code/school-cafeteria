from django.contrib import admin

from django.contrib import admin
from .models import Product, Dish, Menu, Order, PurchaseRequest

admin.site.register(Product)
admin.site.register(Dish)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(PurchaseRequest)
