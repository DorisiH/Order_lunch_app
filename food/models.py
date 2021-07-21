from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FoodMenu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ManyToManyField('Category', related_name='item')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    
class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    items = models.ManyToManyField('FoodMenu', related_name='order', blank=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        db_table = "food_ordermodel"

    def __str__(self):
        return f'Employee: {self.employee} orderd on {self.created_on.strftime("%b %d %I: %M %p")}'
