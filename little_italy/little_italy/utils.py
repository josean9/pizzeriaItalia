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

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Lanza una excepción si ocurre un error HTTP
        data = response.json()

        # Si el ingrediente no existe, lo creamos
        ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)
        ingredient.calories = data.get('calories', 0)
        ingredient.carbs = data.get('totalNutrients', {}).get('CHOCDF', {}).get('quantity', 0)
        ingredient.protein = data.get('totalNutrients', {}).get('PROCNT', {}).get('quantity', 0)
        ingredient.fat = data.get('totalNutrients', {}).get('FAT', {}).get('quantity', 0)
        ingredient.save()

        return ingredient

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de Edamam: {e}")
        return None
