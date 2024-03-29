from django.core.validators import RegexValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=False)
    color = models.CharField(
        max_length=8,
        validators=[RegexValidator(
            regex=r'^#[\d|A-Z]{6}$',
            message='Цвет должен быть в HEX формате, прим: #49B64E')],
        unique=True,
        blank=False)
    slug = models.SlugField(
        max_length=200,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message=' Должно состоять из латинских букв и цифр')],
        unique=True,
        blank=False)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=False)
    measurement_unit = models.CharField(max_length=200, blank=False)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reciepts')
    name = models.CharField(max_length=200, unique=True, blank=False)
    tags = models.ManyToManyField(Tag, blank=False)
    image = models.ImageField(blank=True)
    text = models.TextField(blank=False)
    cooking_time = models.PositiveIntegerField(blank=False)
    ingredients = models.ManyToManyField(
        Ingredient, through="Component",
        blank=False)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='is_favorited')
    is_favorited = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorited_recipe')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'is_favorited'],
                name='unique_user_is_favorited'
            ),
        ]

    def __str__(self) -> str:
        return self.is_favorited.name


class Component(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='components'
        )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.DO_NOTHING)
    quantity = models.FloatField(blank=False)

    class Meta:
        verbose_name = 'Компонент'
        verbose_name_plural = 'Компоненты'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            ),
        ]
