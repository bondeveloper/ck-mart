import json
from .models import *

def cookieCart ( request ):
    try:
        cart = json.loads( request.COOKIES['cart'] )
    except:
        cart = {}

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False }
    cartItems = order['get_cart_items']

    for j in cart:
        try:
            cartItems += cart[j]['quantity']

            product = Product.objects.get(id=j)
            total = ( product.price * cart[j]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[j]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart[j]['quantity'],
                'get_total': total
            }

            items.append( item )
        except:
            pass

    if ( len( items ) > 0 ):
            order['shipping'] = True

    return { 'items': items, 'order': order, 'cartItems': cartItems }

def cartData( request ):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create( customer=customer, complete=False )
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart( request )
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']

    return  { 'items': items, 'order': order, 'cartItems': cartItems }