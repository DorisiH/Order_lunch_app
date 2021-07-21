from django.contrib import admin
from .models import FoodMenu, Category, OrderModel

admin.site.register(FoodMenu)
admin.site.register(Category)
admin.site.register(OrderModel)

