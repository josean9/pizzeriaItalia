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

            return render(request, 'little_italy/cart.html')
    

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    order = Order.objects.filter(user=request.user, status="Preparing").first()
    total = sum(item.total_price for item in order.orderitem_set.all()) if order else 0

    return render(request, 'little_italy/checkout.html', {'total': total})

    


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
            exact_cash = request.POST.get('exact_cash', False) == "on"  # Si está seleccionado, será True
            cash_amount = request.POST.get('cash_amount')

            # Validar solo si el monto exacto no está seleccionado
            if not exact_cash and not cash_amount:
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



from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem

@login_required
def confirm_order(request):
    if request.method == "POST":
        try:
            order = Order.objects.get(user=request.user, status="Preparing")
            order_items = order.orderitem_set.all()

            if not order_items:
                return redirect("cart")

            # Calcular el tiempo de entrega estimado
            total_pizzas = sum(item.quantity for item in order_items)
            estimated_time = datetime.now() + timedelta(minutes=15 * total_pizzas)

            # Actualizar el pedido
            order.status = "On the Way"
            order.save()

            # Vaciar el carrito
            order.orderitem_set.all().delete()

            # Pasar información al template
            return render(request, "little_italy/order_status.html", {
                "order": order,
                "estimated_time": estimated_time,
            })

        except Order.DoesNotExist:
            return redirect("cart")
    return redirect("checkout")


from django.utils.timezone import now
from datetime import timedelta


from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.timezone import now, timedelta
from .models import Order, OrderItem, Pizza

def cart_view(request):
    cart_orders = Order.objects.filter(user=request.user, status="Preparing")
    context = {
        'cart_orders': cart_orders,
    }
    return render(request, 'little_italy/cart.html', context)

def checkout_confirm(request):
    if request.method == "POST":
        try:
            order = Order.objects.get(user=request.user, status="Preparing")

            # Clear cart items
            order.status = "On the Way"
            order.save()

            # Redirect to order status
            return redirect('order_status')

        except Order.DoesNotExist:
            return HttpResponseBadRequest("No order found to confirm.")

    return HttpResponseBadRequest("Invalid request method.")

from datetime import timedelta
from django.utils.timezone import now

def order_status(request):
    try:
        # Obtén la última orden del usuario en estado "En camino"
        order = Order.objects.filter(user=request.user, status="On the Way").latest('created_at')
        total_price = sum(
            item.quantity * (
                item.pizza.price_small if item.size == 'small' else 
                item.pizza.price_medium if item.size == 'medium' else 
                item.pizza.price_large
            ) for item in order.orderitem_set.all()
        )
        
        # Lógica de estimación de tiempo según tamaños
        items = order.orderitem_set.all()
        sizes = [item.size for item in items]
        max_time = 25 if "small" in sizes else 45
        max_time += 15 if "medium" in sizes else 0
        max_time += 30 if "large" in sizes else 0

        # Calcula el rango de tiempo estimado
        current_time = now()
        estimated_time_start = current_time + timedelta(minutes=max_time)
        estimated_time_end = current_time + timedelta(minutes=max_time + 20)

        context = {
            'order': order,
            'total_price': total_price,
            'estimated_time': f"{estimated_time_start.strftime('%H:%M')} y las {estimated_time_end.strftime('%H:%M')}",
        }
    except Order.DoesNotExist:
        context = {'order': None}

    return render(request, 'little_italy/order_status.html', context)
