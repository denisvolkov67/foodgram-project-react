from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_subscribed = models.BooleanField(
        verbose_name="Состояние подписки",
        default=False,
    )

    def __str__(self):
        return self.username
