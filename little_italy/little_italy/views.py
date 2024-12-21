from django.shortcuts import render
from .models import *
from .utils import fetch_nutrition_data


def home_view(request):
    """Vista para la página principal de Little Italy."""
    return render(request, 'home.html')



def menu_view(request):
    """Vista que muestra el menú interactivo de pizzas."""
    pizzas = Pizza.objects.prefetch_related('ingredients')

    # Si se pasa un ingrediente como consulta, busca su información nutricional
    ingredient_name = request.GET.get('ingredient')
    nutrition_data = None
    if ingredient_name:
        nutrition_data = fetch_nutrition_data(ingredient_name)

    return render(request, 'menu.html', {
        'pizzas': pizzas,
        'nutrition_data': nutrition_data
    })


def cart_view(request):
    # Lógica para mostrar el carrito del usuario actual
    return render(request, 'cart.html')


def order_status_view(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'order_status.html', {'order': order})
