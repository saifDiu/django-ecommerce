from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from .models import *
# Create your views here.

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        orders, created = order.objects.get_or_create(customer=customer, complete=False)
        items = orders.orderitem_set.all()
        cartitems = orders.get_cart_items

    else:
        items = []
        orders = {'get_cart_items':0, 'get_cart_total':0}
        cartitems = order['get_cart_items']
    products = product.objects.all()
    context = {'products':products, 'cartitems':cartitems}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        orders, created = order.objects.get_or_create(customer=customer, complete=False)
        items = orders.orderitem_set.all()
        cartitems = orders.get_cart_items

    else:
        items = []
        orders = {'get_cart_items':0, 'get_cart_total':0}
        cartitems = order['get_cart_items']



    context = {'items':items, 'orders':orders, 'cartitems':cartitems}

    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        orders, created = order.objects.get_or_create(customer=customer, complete=False)
        items = orders.orderitem_set.all()
        cartitems = orders.get_cart_items

    else:
        items = []
        orders = {'get_cart_items':0, 'get_cart_total':0}
        cartitems = order['get_cart_items']



    context = {'items':items, 'orders':orders, 'cartitems':cartitems}
    return render(request, 'store/checkout.html', context)


def updateorder(request):

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(productId)
    print(action)

    customer = request.user.customer
    print(customer)

    products = product.objects.get(id=productId)
    print(products)

    orders, created = order.objects.get_or_create(customer=customer, complete=False)

    print(orders.customer)

    orderitems, created = orderitem.objects.get_or_create(order=orders, product=products)
    print(orderitems.quantity)

    if action == 'add':
        orderitems.quantity = (orderitems.quantity + 1)
    elif action == 'remove':
        orderitems.quantity = (orderitems.quantity - 1)

    orderitems.save()

    if orderitems.quantity <= 0:
        orderitems.delete()

    return JsonResponse('Item added Successfully..', safe=False)
