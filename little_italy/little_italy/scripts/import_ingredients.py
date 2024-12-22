import os
import django

# Configuración del entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pizzeriaItalia.settings')
django.setup()

from little_italy.utils import *

def import_ingredients():
    """Importa una lista de ingredientes usando la API de Edamam."""
    ingredients = [
        "1 large apple",
        "1 tomato",
        "200g mozzarella cheese",
        "100g pepperoni",
        "50g mushrooms",
        "50g onions"
    ]

    for ingredient_name in ingredients:
        print(f"Importando: {ingredient_name}...")
        ingredient = fetch_nutrition_data(ingredient_name)
        if ingredient:
            print(f"✔ Ingrediente importado: {ingredient.name} - Calorías: {ingredient.calories}")
        else:
            print(f"✖ Error al importar: {ingredient_name}")

if __name__ == "__main__":
    import_ingredients()
