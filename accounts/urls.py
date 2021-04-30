from django.urls import path

from .views import AccountRegisterView
from . import views

urlpatterns = [
    path('register/', AccountRegisterView.as_view(), name='register'), 
    # path('signin/', views.signin, name='signin'),
    # path('signup/', views.signup, name='signup'),
]
