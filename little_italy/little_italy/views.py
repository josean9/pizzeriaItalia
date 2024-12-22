from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Pizza, Order
from .utils import *

def home_view(request):
    """Vista para la página principal de Little Italy."""
    return render(request, 'little_italy/home.html')

def menu_view(request):
    """Vista que muestra el menú interactivo de pizzas."""
    pizzas = Pizza.objects.prefetch_related('ingredients')
    return render(request, 'little_italy/menu.html', {'pizzas': pizzas})


@login_required
def cart_view(request):
    """Vista para mostrar el carrito del usuario."""
    return render(request, 'little_italy/cart.html')

def login_view(request):
    """Vista para iniciar sesión."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'little_italy/login.html', {'error': 'Usuario o contraseña incorrectos.'})
    return render(request, 'little_italy/login.html')

def logout_view(request):
    """Vista para cerrar sesión."""
    logout(request)
    return redirect('home')


@login_required
def order_status_view(request):
    """Vista para mostrar el estado del pedido del usuario."""
    # Obtiene el último pedido del usuario autenticado
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'little_italy/order_status.html', context)
