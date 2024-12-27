from django.db import models

class Pizza(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price_small = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    price_medium = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    price_large = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    ingredients_small = models.ManyToManyField('Ingredient', related_name='small_pizzas', blank=True)
    ingredients_medium = models.ManyToManyField('Ingredient', related_name='medium_pizzas', blank=True)
    ingredients_large = models.ManyToManyField('Ingredient', related_name='large_pizzas', blank=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    calories = models.FloatField(null=True, blank=True)
    carbs = models.FloatField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True)
    fat = models.FloatField(null=True, blank=True)
    potassium = models.FloatField(null=True, blank=True)  

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    pizzas = models.ManyToManyField(Pizza, through='OrderItem')
    status = models.CharField(
        max_length=20,
        choices=[
            ('Preparing', 'Preparing'),
            ('On the Way', 'On the Way'),
            ('Delivered', 'Delivered'),
        ],
        default='Preparing',
    )
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(
        max_length=6,
        choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')],
        default='small',
    )

    @property
    def total_price(self):
        if self.size == 'small':
            return self.quantity * self.pizza.price_small
        elif self.size == 'medium':
            return self.quantity * self.pizza.price_medium
        elif self.size == 'large':
            return self.quantity * self.pizza.price_large
        return 0
