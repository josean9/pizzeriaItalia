# Generated by Django 4.2.17 on 2024-12-22 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('little_italy', '0002_ingredient_potassium'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pizza',
            name='ingredients',
        ),
        migrations.RemoveField(
            model_name='pizza',
            name='price',
        ),
        migrations.RemoveField(
            model_name='pizza',
            name='size',
        ),
        migrations.AddField(
            model_name='pizza',
            name='ingredients_large',
            field=models.ManyToManyField(blank=True, related_name='large_pizzas', to='little_italy.ingredient'),
        ),
        migrations.AddField(
            model_name='pizza',
            name='ingredients_medium',
            field=models.ManyToManyField(blank=True, related_name='medium_pizzas', to='little_italy.ingredient'),
        ),
        migrations.AddField(
            model_name='pizza',
            name='ingredients_small',
            field=models.ManyToManyField(blank=True, related_name='small_pizzas', to='little_italy.ingredient'),
        ),
        migrations.AddField(
            model_name='pizza',
            name='price_large',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='pizza',
            name='price_medium',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='pizza',
            name='price_small',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
