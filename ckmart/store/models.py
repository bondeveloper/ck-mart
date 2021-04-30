import uuid
from django.db import models

from accounts.models import Account


class Product( models.Model ):
    name = models.CharField( max_length=200 )
    description = models.CharField( null=True, blank=True, max_length=200 )
    price = models.DecimalField( max_digits=7, decimal_places=2 )
    image = models.ImageField( default='placeholder.png', blank=True )

    def __str__( self ):
        return self.name

    @property
    def imageURL( self ):
        try:
            url = self.image.url
        except:
            url = ''

        return url


class Order( models.Model ):
    transaction_id = models.UUIDField( default=uuid.uuid4, editable=False, unique=True )
    account = models.ForeignKey( Account, null=True, blank=True, on_delete=models.SET_NULL )
    date_ordered = models.DateField( auto_now_add=True )
    complete = models.BooleanField( default=False )
    
    STATUS = (
        ('UP', 'Un Processed'),
        ('P', 'Paid'),
        ('PR', 'Processing'),
        ('HC', 'Handed to Courier'),
        ('OD', 'Out on delivery'),
        ('D', 'Delivered'),
        ('C', 'Cancelled')
    )
    status = models.CharField( max_length=3, choices=STATUS, default='UP' )

    def __str__( self ):
        return str( self.transaction_id )

    def __unicode__( self ):
        return str( self.transaction_id )

    @property
    def canShip( self ):
        shouldShip = False
        orderitems = self.orderitem_set.all()

        if orderitems:
            shouldShip = True
        return shouldShip

    @property
    def get_cart_total( self ):
        orderitems = self.orderitem_set.all()
        total = sum( [item.get_total for item in orderitems] )
        return total

    @property
    def get_cart_items( self ):
        orderitems = self.orderitem_set.all()
        total = sum( [item.quantity for item in orderitems] )
        return total


class Shipping( models.Model ):
    order = models.ForeignKey( Order, on_delete=models.CASCADE )
    recipient_name = models.CharField( max_length=200 )
    contact_number = models.CharField( max_length=50 )
    address_line1 = models.CharField( max_length=200 )
    address_line2 = models.CharField( max_length=200, null=True, blank=True )
    surburb = models.CharField( max_length=200 )
    city = models.CharField( max_length=200 )
    postal_code = models.CharField( max_length=200 )
    instructions = models.CharField( max_length=200, null=True, blank=True)

    def __str__( self ):
        return self.order.__str__() + " : " + self.recipient_name


class OrderItem( models.Model ):
    product = models.ForeignKey( Product, null=True, on_delete=models.SET_NULL )
    order = models.ForeignKey( Order, null=True, on_delete=models.SET_NULL )
    quantity = models.IntegerField( default=0, null=True, blank=True )
    date_added = models.DateField( auto_now_add=True )

    class Meta:
        # models.UniqueConstraint(fields=['product', 'order'], name='unique_order_item')
        constraints = [
            models.UniqueConstraint(fields=['product', 'order'], name='unique_order_item')
        ]

    def __str__( self ):
        return self.product.name

    @property
    def get_total( self ):
        total = self.product.price * self.quantity
        return total



