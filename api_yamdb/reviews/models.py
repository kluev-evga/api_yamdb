from django.contrib.auth.models import AbstractUser
from django.db import models


class Categories(models.Model):
    name = models.CharField(
        'Имя категории',
        max_length=256,
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:25]


class Genres(models.Model):
    name = models.CharField(
        'Название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:25]


class Titles(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=256,
    )
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.DO_NOTHING,
        related_name='category',
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genres,
        through='GenreTitle',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:25]


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
            self.role = 'admin'
        super().save(*args, **kwargs)


SCORE = [
    (1, '1'), (2, '2'), (3, '3'),
    (4, '4'), (5, '5'), (6, '6'),
    (7, '7'), (8, '8'), (9, '9'), (10, '10')
]


class Reviews(models.Model):
    title = models.ForeignKey(
        Titles,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        choices=SCORE
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text[:25]


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genres,
        on_delete=models.DO_NOTHING,
        verbose_name='Название жанра',
        related_name='genres'
    )
    title = models.ForeignKey(
        Titles,
        on_delete=models.DO_NOTHING,
        verbose_name='Название произведения',
        related_name='titles'
    )

    def __str__(self):
        return f'{self.genre} {self.title}'
