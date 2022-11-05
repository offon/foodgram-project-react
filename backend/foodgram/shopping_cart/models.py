from django.db import models
from recipes.models import Recipe
from users.models import User


class IsInShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='is_in_shopping_cart')
    is_in_shopping_cart = models.ForeignKey(
        Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Добавлен в корзину'
        verbose_name_plural = 'Добавлены в корзину'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'is_in_shopping_cart'],
                name='unique_user_is_in_shopping_cart'
            ),
        ]

    def __str__(self) -> str:
        return self.is_in_shopping_cart.name
