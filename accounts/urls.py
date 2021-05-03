from django.urls import path

from .views import AccountRegisterView, AccountUpdateView
from . import views

urlpatterns = [
    path('register/', AccountRegisterView.as_view(), name='register'), 
    path('profile/<int:pk>', AccountUpdateView.as_view(), name='profile'),
    path('profile/', views.profile, name='profile2'),
]
