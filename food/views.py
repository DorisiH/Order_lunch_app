from django.shortcuts import render
from django.views import View
from .models import FoodMenu, OrderModel, Category
from django.contrib.auth.models import User
from django.views.generic import ListView
import datetime
from  datetime import date
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'food/base.html')

class Profile(View):
    def get(self, request, *args, **kwargs):
        current_user = request.user
        items = request.POST.getlist('items[]')
        useri = OrderModel.objects.filter(employee__username__contains=current_user)
        context = {
            'useri': useri
        }
        
        return render(request, 'users/profile.html', context)
            
#class OrderListView(ListView):
 #   model = OrderModel
#    template_name = 'users/ordered_list.html'
        
def orderList(request):
    #response = HttpResponse(content_type='text/csv')
    #response['Content-Disposition'] = 'attachment; filename=ordered_list1.csv'

    if request.method=='POST':
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        searchresult = OrderModel.objects.raw('select employee_id, id ,price, date, created_on from food_ordermodel where date between "'+fromdate+'" and "'+todate+'"')
        food_items = OrderModel.objects.raw('select id, from food_ordermodel_items')
        context = {
            'searchresult': searchresult,
            'food_items': food_items,
        }
        
        writer = csv.writer(response)
        datat = OrderModel.objects.all() 
        writer.writerow(['Name', 'Items', 'Price', 'Date'])
        for y in searchresult:
            writer.writerow([y.employee, y.items, y.price, y.date])
        return response
        
        return render(request, 'users/ordered_list.html', context)
    else:
        displaydata = OrderModel.objects.all()
        context = {
            'displaydata': displaydata
        }
        return render(request, 'users/ordered_list.html', context)

# def export_csv(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename=venues.csv'
    
#     writer = csv.writer(response)
#     datat = OrderModel.objects.all() 
#     writer.writerow(['Date', 'Items', 'Price'])

#     for y in data:
#         writer.writerow([data.date, data.price, data.items])
#     return response


class Order(View):
    def get(self, request, *args, **kwargs):
        soup = FoodMenu.objects.filter(category__name__contains='soup')
        dessert = FoodMenu.objects.filter(category__name__contains='dessert')
        drink = FoodMenu.objects.filter(category__name__contains='drink')
        tjera = FoodMenu.objects.filter(category__name__contains='tjera')
        
        context = {
            'soup': soup,
            'dessert': dessert,
            'drink': drink,
            'tjera': tjera,
        }   
        
        return render(request, 'food/order.html', context)


    def post(self, request, *args, **kwargs):
            order_items = {
                'items': []
            }

            items = request.POST.getlist('items[]')

            for item in items:
                menu_item = FoodMenu.objects.get(pk__contains=int(item))
                item_data = {
                    'id': menu_item.pk,
                    'name': menu_item.name,
                    'price': menu_item.price
                }

                order_items['items'].append(item_data)

                price = 0
                item_ids = []


            for item in order_items['items']:
                price += item['price']   
                item_ids.append(item['id'])

            current_user = request.user
            current_date = date.today()

            punonjesi = OrderModel.objects.filter(employee__username__contains=current_user)
        
            for x in punonjesi:
                if x.date == date.today(): 
                    return render(request, 'food/ordered_today.html')

            if price > 5:
                return render(request, 'food/order_notacepted.html')
            else:  
            
                order = OrderModel.objects.create(price=price, employee=current_user)  
                order.items.add(*item_ids)
                context = {
                    'items': order_items['items'],
                    'price': price
                }
                

                return render(request, 'food/order_confirmation.html', context)

#Kristi Dalipaj17:07
#for category in Category.objects.all(): context[category.name] = FoodMenu..objects.filter(categroy__name__contains='category.name'