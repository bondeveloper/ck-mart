from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _

class AccountManager( BaseUserManager ):
    def create_user( self, email, password, **kwargs ):

        if not email:
            raise ValueError( _( 'You need to provide an email' ) )
        email = self.normalize_email( email )
        account = self.model( email=email, **kwargs )
        account.set_password( password )
        account.save( using=self._db )

        return account

    def create_superuser( self, email, password, **kwargs ):

        kwargs.setdefault( 'is_staff', True )
        kwargs.setdefault( 'is_superuser', True )
        kwargs.setdefault( 'is_active', True )

        if kwargs.get('is_staff') is not True:
            raise ValueError( _( 'Superuser staff field should be true'))

        if kwargs.get('is_superuser') is not True:
            raise ValueError( _( 'Superuser is_superuser field should be true'))

        if kwargs.get('is_active') is not True:
            raise ValueError( _( 'Superuser active field should be true'))

        return self.create_user( email, password, **kwargs )


class Account( AbstractBaseUser, PermissionsMixin ):

    email = models.EmailField( _('email address'), unique=True )
    password = models.CharField( max_length=200 )
    first_name = models.CharField( max_length=200 )
    last_name = models.CharField( max_length=200, null=True )
    phone = models.CharField( max_length=200 )
    created_at = models.DateTimeField( auto_now_add=True )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    objects = AccountManager()

    def __str__(self):
        return self.email


class Address( models.Model ):
    account = models.ForeignKey( Account, null=True, blank=True, on_delete=models.SET_NULL )
    address = models.CharField( max_length=200, null=True, blank=True )
    city = models.CharField( max_length=200, null=True, blank=True )
    postal_code = models.CharField( max_length=200, null=True, blank=True )
    created_at = models.DateTimeField( auto_now_add=True )
    isDefault = models.BooleanField( default=False )

    def __str__( self ):
        return self.address