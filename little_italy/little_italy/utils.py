import requests
from django.conf import settings
from .models import Pizza, Ingredient


def fetch_pizzas_from_api():
    """Obtiene información de pizzas con diferentes tamaños y guarda en la base de datos."""
    url = "https://api.edamam.com/api/nutrition-data"
    params = {
        "app_id": settings.EDAMAM_APP_ID,
        "app_key": settings.PIZZA_KEY,
    }

    sample_pizzas = [
        {
            "name": "Margarita",
            "description": "Pizza clásica con queso, tomate y masa.",
            "sizes": {
                "S": {"price": 8.0, "ingredients": ["150g pizza dough", "75g mozzarella cheese", "150g tomato", "7g basil"]},
                "M": {"price": 10.0, "ingredients": ["200g pizza dough", "100g mozzarella cheese", "200g tomato", "10g basil"]},
                "L": {"price": 12.0, "ingredients": ["250g pizza dough", "125g mozzarella cheese", "250g tomato", "15g basil"]},
            }
        },
    ]

    try:
        for pizza_data in sample_pizzas:
            for size, size_data in pizza_data['sizes'].items():
                ingredients = []
                for ingredient_text in size_data['ingredients']:
                    response = requests.get(url, params={**params, "ingr": ingredient_text})
                    if response.status_code == 200:
                        nutrition_data = response.json()
                        ingredient, _ = Ingredient.objects.get_or_create(
                            name=ingredient_text,
                            defaults={
                                'calories': nutrition_data.get('calories', 0),
                                'carbs': nutrition_data['totalNutrients'].get('CHOCDF', {}).get('quantity', 0),
                                'protein': nutrition_data['totalNutrients'].get('PROCNT', {}).get('quantity', 0),
                                'fat': nutrition_data['totalNutrients'].get('FAT', {}).get('quantity', 0),
                                'potassium': nutrition_data['totalNutrients'].get('K', {}).get('quantity', 0),
                            }
                        )
                        ingredients.append(ingredient)

                pizza_obj, _ = Pizza.objects.get_or_create(
                    name=f"{pizza_data['name']} ({size})",
                    defaults={
                        'description': pizza_data['description'],
                        'price': size_data['price'],
                    }
                )
                pizza_obj.ingredients.set(ingredients)
                pizza_obj.save()

        print("Pizzas importadas correctamente.")
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")


def test_api_request():
    """Prueba directa de la API de Edamam con un ingrediente simple."""
    url = "https://api.edamam.com/api/nutrition-data"
    params = {
        "app_id": "44eac434",  # Reemplaza por tu APP ID
        "app_key": "7aa07d9c0e5ed65ffbda76b01eadbd6b",  # Reemplaza por tu APP KEY
        "ingr": "1 large apple"  # Ingrediente de prueba
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        print("Respuesta de la API:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        if response.status_code == 400:
            print("Detalles del error:", response.text)
