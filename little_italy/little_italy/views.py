from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from .utils import *

def home_view(request):
    """Vista para la página principal de Little Italy."""
    return render(request, 'little_italy/home.html')
import json
from django.core.serializers.json import DjangoJSONEncoder

from django.http import JsonResponse

from django.shortcuts import render, get_object_or_404

def pizza_details_view(request, pizza_id, size):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    if size == 'small':
        ingredients = pizza.ingredients_small.all()
        price = pizza.price_small
    elif size == 'medium':
        ingredients = pizza.ingredients_medium.all()
        price = pizza.price_medium
    elif size == 'large':
        ingredients = pizza.ingredients_large.all()
        price = pizza.price_large
    else:
        ingredients = []
        price = 0

    context = {
        'pizza': pizza,
        'size': size.capitalize(),
        'price': price,
        'ingredients': ingredients,
    }
    return render(request, 'little_italy/pizza_details.html', context)


def menu_view(request):
    pizzas = Pizza.objects.prefetch_related(
        'ingredients_small', 'ingredients_medium', 'ingredients_large'
    )
    pizzas_list = []
    for pizza in pizzas:
        pizzas_list.append({
            'id': pizza.id,
            'name': pizza.name,
            'description': pizza.description,
            'price_small': pizza.price_small,
            'price_medium': pizza.price_medium,
            'price_large': pizza.price_large,
            'ingredients_small': [
                {
                    'name': ing.name,
                    'calories': ing.calories,
                    'potassium': ing.potassium,
                } for ing in pizza.ingredients_small.all()
            ],
            'ingredients_medium': [
                {
                    'name': ing.name,
                    'calories': ing.calories,
                    'potassium': ing.potassium,
                } for ing in pizza.ingredients_medium.all()
            ],
            'ingredients_large': [
                {
                    'name': ing.name,
                    'calories': ing.calories,
                    'potassium': ing.potassium,
                } for ing in pizza.ingredients_large.all()
            ],
        })

    return render(request, 'little_italy/menu.html', {
        'pizzas': pizzas,
        'pizzas_json': json.dumps(pizzas_list, cls=DjangoJSONEncoder)
    })


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

from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages


@login_required(login_url='/login/')  # Redirigir a la página de inicio de sesión
def add_to_cart(request):
    if request.method == "POST":
        pizza_id = request.POST.get("pizza_id")
        size = request.POST.get("size")
        
        if not pizza_id or not size:
            return HttpResponseBadRequest("Pizza ID and size are required.")

        try:
            pizza = Pizza.objects.get(id=pizza_id)
        except Pizza.DoesNotExist:
            return JsonResponse({"error": "Pizza not found"}, status=404)

        # Obtener el precio basado en el tamaño
        if size == "small":
            price = pizza.price_small
        elif size == "medium":
            price = pizza.price_medium
        elif size == "large":
            price = pizza.price_large
        else:
            return JsonResponse({"error": "Invalid size selected"}, status=400)

        if not price:
            return JsonResponse({"error": "Price for the selected size is not available"}, status=400)

        # Obtener o crear la orden del usuario
        order, created = Order.objects.get_or_create(user=request.user, status="Preparing")

        # Agregar el item a la orden
        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            pizza=pizza,
            size=size,
        )
        if not created:
            order_item.quantity += 1
            order_item.save()

        return render(request, 'little_italy/cart.html')

    # Si no está autenticado, redirigir a login con un mensaje
    messages.error(request, "Debes iniciar sesión para agregar pizzas al carrito.")
    return redirect('/login/')  # Cambia la URL al path de tu página de login


def remove_from_cart(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        item = get_object_or_404(OrderItem, id=item_id)

        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()

            return redirect("cart")
        """return render(request, 'little_italy/cart.html')
    """

def checkout(request):
    if request.method == "GET":
        return render(request, "little_italy/checkout.html")
    


def process_order(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        if not address or not payment_method:
            return JsonResponse({"error": "Address and payment method are required"}, status=400)

        # Validación de campos adicionales según el método de pago
        if payment_method == "credit_card":
            card_number = request.POST.get('card_number')
            cvc = request.POST.get('cvc')
            expiry_date = request.POST.get('expiry_date')
            if not card_number or not cvc or not expiry_date:
                return JsonResponse({"error": "Complete credit card details are required"}, status=400)

        elif payment_method == "paypal":
            paypal_email = request.POST.get('paypal_email')
            if not paypal_email:
                return JsonResponse({"error": "PayPal email is required"}, status=400)

        elif payment_method == "cash":
            cash_amount = request.POST.get('cash_amount')
            exact_cash = request.POST.get('exact_cash', False)
            if not cash_amount:
                return JsonResponse({"error": "Cash amount is required"}, status=400)

        # Actualizar el pedido
        try:
            order = Order.objects.get(user=request.user, status="Preparing")
        except Order.DoesNotExist:
            return JsonResponse({"error": "No active order found"}, status=404)

        order.status = "On the Way"
        order.save()

        return redirect('order_status')

    return JsonResponse({"error": "Invalid request method"}, status=400)
