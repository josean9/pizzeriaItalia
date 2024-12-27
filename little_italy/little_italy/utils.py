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
    },
    {
        "name": "Pepperoni",
        "description": "Pizza con queso, tomate y pepperoni.",
        "base_price": 12.0,
        "sizes": {
            "S": ["150g pizza dough", "75g mozzarella cheese", "150g tomato", "50g pepperoni"],
            "M": ["200g pizza dough", "100g mozzarella cheese", "200g tomato", "70g pepperoni"],
            "L": ["300g pizza dough", "150g mozzarella cheese", "300g tomato", "100g pepperoni"],
        },
    },
    {
        "name": "Hawaiana",
        "description": "Pizza con queso, tomate, piña y jamón.",
        "base_price": 11.0,
        "sizes": {
            "S": ["150g pizza dough", "75g mozzarella cheese", "150g tomato", "50g pineapple", "50g ham"],
            "M": ["200g pizza dough", "100g mozzarella cheese", "200g tomato", "70g pineapple", "70g ham"],
            "L": ["300g pizza dough", "150g mozzarella cheese", "300g tomato", "100g pineapple", "100g ham"],
        },
    },
    {
        "name": "Vegetariana",
        "description": "Pizza con queso, tomate y vegetales frescos.",
        "base_price": 11.5,
        "sizes": {
            "S": ["150g pizza dough", "75g mozzarella cheese", "150g tomato", "50g bell peppers", "30g mushrooms", "30g olives"],
            "M": ["200g pizza dough", "100g mozzarella cheese", "200g tomato", "70g bell peppers", "50g mushrooms", "50g olives"],
            "L": ["300g pizza dough", "150g mozzarella cheese", "300g tomato", "100g bell peppers", "70g mushrooms", "70g olives"],
        },
    },
    {
        "name": "Cuatro Quesos",
        "description": "Pizza con una mezcla de cuatro quesos.",
        "base_price": 13.0,
        "sizes": {
            "S": ["150g pizza dough", "50g mozzarella cheese", "50g cheddar cheese", "50g parmesan cheese", "50g blue cheese"],
            "M": ["200g pizza dough", "70g mozzarella cheese", "70g cheddar cheese", "70g parmesan cheese", "70g blue cheese"],
            "L": ["300g pizza dough", "100g mozzarella cheese", "100g cheddar cheese", "100g parmesan cheese", "100g blue cheese"],
        },
    },
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
