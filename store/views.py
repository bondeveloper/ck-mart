from django.shortcuts import render
from .models import *
from django.http import JsonResponse, HttpResponse
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

    account = request.user 
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(account=account, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        quantity = int( data.get('quantity') )
        orderItem.quantity = (orderItem.quantity + quantity )
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder( request ):
    data = json.loads( request.body )

    if request.user.is_authenticated:
        account = request.user
        try:
            order = Order.objects.get(account=account)
            order.transaction_id = datetime.datetime.now().timestamp()

            if float( data.get('data').get('total') ) == order.get_cart_total:
                order.complete = True

            order.save()

            if order.shipping == True:
                ShippingAddress.objects.create(
                    account=account,
                    order=order,
                    address=data.get('data').get('address'),
                    city=data.get('data').get('city'),
                    postal_code=data.get('data').get('postal_code')
                )
        except:
            print('process order error occured')

       
    else:
        print('User is not logged in!')
    return JsonResponse('Payment complete', safe=False)

def product( request, id ):
    product = Product.objects.get(id=id)

    data = cartData( request )
    cartItems = data['cartItems']

    context = { 'product': product, 'cartItems': cartItems }
    return render(request, 'store/product.html', context)

def orders( request ):

    orders = Order.objects.filter(account=request.user.pk)
    data = cartData( request )
    cartItems = data['cartItems']

    context = { 'orders': orders, 'cartItems': cartItems }

    return render(request, 'store/orders.html', context)

def order( request, id ):

    order = Order.objects.get(id=id)
    items = order.orderitem_set.all()
    data = cartData( request )
    cartItems = data['cartItems']

    context = { 'order': order, 'cartItems': cartItems, 'items': items }

    return render(request, 'store/order.html', context)