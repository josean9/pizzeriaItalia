# Generated by Django 4.2.17 on 2024-12-22 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('little_italy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='potassium',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
