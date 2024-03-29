# Generated by Django 4.1.3 on 2022-11-02 11:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0006_remove_recipe_is_favorited_favorite_and_more'),
        ('shopping_cart', '0003_auto_20221029_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='isinshoppingcart',
            name='is_in_shopping_cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe'),
        ),
        migrations.AlterField(
            model_name='isinshoppingcart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_in_shopping_cart', to=settings.AUTH_USER_MODEL),
        ),
    ]
