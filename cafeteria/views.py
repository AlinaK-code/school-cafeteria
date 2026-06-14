from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Menu, Order, PurchaseRequest
from django.utils import timezone


# функционал повара (мой вариант)

def home(request):
    return render(request, 'cafeteria/home.html')

@login_required
def cook_dashboard(request):
    # если это не повар, отправляем домой
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'cook':
        return redirect('home')
    
    return render(request, 'cafeteria/cook_dashboard.html')

@login_required
def cook_orders(request):
    # учет выданных завтраков, обедов, напитков и тд
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'cook':
        return redirect('home')

    # тут получаю все заказы, сортирую от новых к старым
    orders = Order.objects.select_related('student', 'menu_item__dish').order_by('-issued_at')
    
    # функционал кнопки "Выдать"
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(id=order_id, is_issued=False)
            order.is_issued = True
            order.issued_at = timezone.now()
            order.save()
            messages.success(request, f"Блюдо '{order.menu_item.dish.name}' успешно выдано!")
        except Order.DoesNotExist:
            messages.error(request, "Ошибка: заказ уже выдан или не найден.")
        return redirect('cook_orders')

    return render(request, 'cafeteria/cook_orders.html', {'orders': orders})

@login_required
def cook_products(request):
    # учет остатков продуктов
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'cook':
        return redirect('home')
    
    products = Product.objects.all().order_by('name')
    return render(request, 'cafeteria/cook_products.html', {'products': products})
    meals = Dish.objects.all().order_by("name")



@login_required
def create_request(request):
    # закупка продуктов
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'cook':
        return redirect('home')
        
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        
        if product_id and quantity:
            product = Product.objects.get(id=product_id)
            PurchaseRequest.objects.create(
                product=product,
                quantity_needed=quantity,
                created_by=request.user
            )
            messages.success(request, "Заявка на закупку успешно отправлена администратору!")
            return redirect('cook_products')
            
    products = Product.objects.all()
    return render(request, 'cafeteria/create_request.html', {'products': products})

