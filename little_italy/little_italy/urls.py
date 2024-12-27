"""
URL configuration for little_italy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('menu/', menu_view, name='menu'),
    path('cart/', cart_view, name='cart'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('order_status/', order_status_view, name='order_status'),
    path('pizza/<int:pizza_id>/<str:size>/', pizza_details_view, name='pizza_details'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    
    
]
