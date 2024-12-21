from django.db import models

class Pizza(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    ingredients = models.ManyToManyField('Ingredient', related_name='pizzas')
    size = models.CharField(max_length=10, choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')])

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    calories = models.FloatField()
    fat = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()

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
    total = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
