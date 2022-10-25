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

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=False)
    measurement_unit = models.CharField(max_length=200, blank=False)

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True, blank=False)
    tags = models.ManyToManyField(Tag, blank=False)
    image = models.ImageField(blank=True)
    text = models.TextField(blank=False)
    cooking_time = models.PositiveIntegerField(blank=False)
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)
    ingredients = models.ManyToManyField(
        Ingredient, through="Component",
        blank=False)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.name


class Component(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
        )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.DO_NOTHING)
    quantity = models.FloatField(blank=False)
