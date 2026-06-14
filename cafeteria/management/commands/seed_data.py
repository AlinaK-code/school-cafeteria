from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.utils import timezone
from datetime import timedelta, date
from django.contrib.auth.models import User
from cafeteria.models import Product, Dish, Menu, Order, PurchaseRequest, Profile

fake = Faker("ru_RU")

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        
        self.create_products(25)
        self.create_dishes(20)
        self.create_menu(30)
        self.create_users(25) 
        self.create_orders(40)
        self.create_purchase_requests(15)
        
        self.stdout.write(self.style.SUCCESS('База данных успешно наполнена!'))

    def create_products(self, number):
        products_list = [
            "Картофель", "Морковь", "Лук репчатый", "Куриное филе", "Говядина",
            "Рис", "Гречка", "Макароны", "Молоко", "Сметана",
            "Мука пшеничная", "Сахар", "Яйца куриные", "Масло сливочное", "Хлеб белый",
            "Капуста", "Свекла", "Яблоки", "Бананы", "Компот ягодный"
        ]
        for name in products_list[:number]:
            Product.objects.get_or_create(
                name=name,
                defaults={
                    'quantity': round(random.integer(10, 100), 2),
                    'unit': random.choice(['кг', 'л', 'шт'])
                }
            )

    def create_dishes(self, number):
        dishes_list = [
            ("Борщ", 'lunch', 120.00), ("Котлета по-киевски", 'lunch', 150.00),
            ("Пюре картофельное", 'lunch', 60.00), ("Салат Оливье", 'lunch', 90.00),
            ("Омлет с сыром", 'breakfast', 80.00), ("Каша овсяная", 'breakfast', 50.00),
            ("Блины со сметаной", 'breakfast', 70.00), ("Сырники", 'breakfast', 85.00),
            ("Суп куриный", 'lunch', 110.00), ("Макароны с сыром", 'lunch', 95.00),
            ("Тефтели", 'lunch', 130.00), ("Винегрет", 'lunch', 75.00),
            ("Гренки с чесноком", 'breakfast', 40.00), ("Творожная запеканка", 'breakfast', 90.00),
            ("Плов", 'lunch', 140.00), ("Щи из свежей капусты", 'lunch', 100.00),
            ("Рыба запеченная", 'lunch', 160.00), ("Рисовая каша", 'breakfast', 55.00),
            ("Сосиска с пюре", 'lunch', 115.00), ("Компот и булочка", 'breakfast', 45.00),
        ]
        for name, d_type, price in dishes_list[:number]:
            Dish.objects.get_or_create(
                name=name,
                defaults={'dish_type': d_type, 'price': price}
            )

    def create_menu(self, number):
        dishes = list(Dish.objects.all())
        if not dishes: return
        
        today = date.today()
        for i in range(number):
            menu_date = today + timedelta(days=i)
            dish = random.choice(dishes)
            Menu.objects.get_or_create(
                date=menu_date,
                dish=dish,
                defaults={'portions_available': random.randint(20, 100)}
            )

    def create_users(self, number):
        # создаю студентов
        for _ in range(number):
            username = fake.unique.user_name()
            user = User.objects.create_user(
                username=username,
                email=fake.email(),
                password='student123'
            )
            Profile.objects.update_or_create(user=user, defaults={'role': 'student'})
        
        # убеждаюсь, что у povar есть профиль
        try:
            povar_user = User.objects.get(username='povar')
            Profile.objects.update_or_create(user=povar_user, defaults={'role': 'cook'})
        except User.DoesNotExist:
            pass

    def create_orders(self, number):
        students = User.objects.filter(profile__role='student')
        menus = Menu.objects.all()
        
        if not students or not menus: return

        for _ in range(number):
            student = random.choice(students)
            menu_item = random.choice(menus)
            
            # типа некоторые заказы уже выданы
            is_issued = random.choice([True, False])
            issued_time = timezone.now() - timedelta(hours=random.randint(1, 48)) if is_issued else None

            Order.objects.create(
                student=student,
                menu_item=menu_item,
                is_issued=is_issued,
                issued_at=issued_time if is_issued else timezone.now()
            )

    def create_purchase_requests(self, number):
        products = Product.objects.all()
        users = User.objects.all()
        
        if not products: return

        for _ in range(number):
            product = random.choice(products)
            creator = random.choice(users)
            PurchaseRequest.objects.create(
                product=product,
                quantity_needed=random.randint(5, 50),
                status=random.choice(['pending', 'approved', 'rejected']),
                created_by=creator
            )