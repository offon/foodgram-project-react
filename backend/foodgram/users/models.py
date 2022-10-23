from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.db import models

username_validator = UnicodeUsernameValidator()


class User(AbstractUser):
    username = models.CharField(
        ('username'),
        max_length=150,
        unique=True,
        validators=[username_validator],
    )
    first_name = models.CharField(('first name'), max_length=150, blank=False)
    last_name = models.CharField(('last name'), max_length=150, blank=False)
    email = models.EmailField(('email address'), max_length=254, blank=False)
    # is_subscribed = models.ManyToManyField('self', through='Follow')


class Follow(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='following')
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author'
            ),
        ]
