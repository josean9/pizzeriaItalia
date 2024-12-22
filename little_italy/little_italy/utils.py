import requests
from django.conf import settings
from .models import Pizza, Ingredient


def fetch_pizzas_from_api():
    # Eliminar todas las pizzas existentes antes de importar nuevas
    Pizza.objects.all().delete()

    url = "https://api.edamam.com/api/nutrition-data"
    params = {
        "app_id": settings.EDAMAM_APP_ID,
        "app_key": settings.PIZZA_KEY,
    }

    sample_pizzas = [
        {
            "name": "Margarita",
            "description": "Pizza clásica con queso, tomate y masa.",
            "base_price": 10.0,
            "sizes": {
                "S": ["150g pizza dough", "75g mozzarella cheese", "150g tomato", "7g basil"],
                "M": ["200g pizza dough", "100g mozzarella cheese", "200g tomato", "10g basil"],
                "L": ["300g pizza dough", "150g mozzarella cheese", "300g tomato", "15g basil"],
            },
        }
    ]

    for pizza_data in sample_pizzas:
        sizes = pizza_data['sizes']
        ingredients_small = []
        ingredients_medium = []
        ingredients_large = []

        for size, ingredient_list in sizes.items():
            for ingredient_text in ingredient_list:
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
                    if size == "S":
                        ingredients_small.append(ingredient)
                    elif size == "M":
                        ingredients_medium.append(ingredient)
                    elif size == "L":
                        ingredients_large.append(ingredient)

        pizza_obj, _ = Pizza.objects.get_or_create(
            name=pizza_data['name'],
            defaults={
                'description': pizza_data['description'],
                'price_small': pizza_data['base_price'],
                'price_medium': pizza_data['base_price'] * 1.5,
                'price_large': pizza_data['base_price'] * 2,
            }
        )
        pizza_obj.ingredients_small.set(ingredients_small)
        pizza_obj.ingredients_medium.set(ingredients_medium)
        pizza_obj.ingredients_large.set(ingredients_large)
        pizza_obj.save()

    print("Todas las pizzas existentes han sido eliminadas e importadas correctamente.")
