import requests
from django.conf import settings
from .models import Ingredient

def fetch_nutrition_data(ingredient_name):
    """Obtiene información nutricional de Edamam y la guarda en el modelo Ingredient."""
    url = "https://api.edamam.com/api/nutrition-data"
    params = {
        "app_id": settings.EDAMAM_APP_ID,
        "app_key": settings.PIZZA_KEY,
        "ingr": ingredient_name
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Si el ingrediente no existe, lo creamos
        ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)
        ingredient.calories = data.get('calories', 0)
        ingredient.carbs = data['totalNutrients'].get('CHOCDF', {}).get('quantity', 0)
        ingredient.protein = data['totalNutrients'].get('PROCNT', {}).get('quantity', 0)
        ingredient.fat = data['totalNutrients'].get('FAT', {}).get('quantity', 0)
        ingredient.save()
        return ingredient
    else:
        return None
