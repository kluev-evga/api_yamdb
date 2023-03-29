from django.contrib.auth.models import AbstractUser
from django.db import models


class Titles(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.DO_NOTHING,
        related_name='category',
        verbose_name='Категория',
    )

    def __str__(self):
        return self.name


ROLES = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
]


class User(AbstractUser):
    bio = models.TextField(
        'биография',
    )
    role = models.CharField(
        'роль пользователя',
        max_length=50,
        choices=ROLES,
    )

    class Meta:
        db_table = "auth_user"

    def save(self, *args, **kwargs):
        """Установить роль при создании superuser"""
        if self.is_superuser:
            self.role = 'moderator'
        super().save(*args, **kwargs)
