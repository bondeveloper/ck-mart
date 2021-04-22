from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cartData

def store( request ):
    data = cartData( request )
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = { 'products': products, 'cartItems': cartItems }
    return render( request, 'store/store.html', context )

def cart( request ):
    data = cartData( request )
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = { 'items': items, 'order': order, 'cartItems': cartItems }
    return render( request, 'store/cart.html', context )

def checkout( request ):
    data = cartData( request )
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = { 'items': items, 'order': order, 'cartItems': cartItems }
    return render( request, 'store/checkout.html', context )

def updateItem( request ):
    data = json.loads( request.body )
    productId = data.get('productId')
    action = data.get('action')

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder( request ):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads( request.body )

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float( data.get('data').get('total') )
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data.get('data').get('address'),
                city=data.get('data').get('city'),
                postal_code=data.get('data').get('postal_code')
            )
    else:
        print('User is not logged in!')
    return JsonResponse('Payment complete', safe=False)