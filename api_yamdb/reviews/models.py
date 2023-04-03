from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy


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
        return self.slug


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
        return self.slug


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


def validate_username(value):
    if value == 'me':
        raise ValidationError('Недопустимое имя пользователя - me')


class User(AbstractUser):
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text=gettext_lazy('Required. 150 characters or fewer.'
                               ' Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator(), validate_username],
        error_messages={
            'unique': gettext_lazy(
                "A user with that username already exists."),
        },
    )
    email = models.EmailField(
        'Email',
        unique=True,
    )
    bio = models.TextField(
        'биография',
        blank=True,
        null=True,
    )
    role = models.CharField(
        'роль пользователя',
        max_length=50,
        choices=ROLES,
        default='user'
    )

    class Meta:
        db_table = "auth_user"
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

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
        return f'{self.genre}'


class Comments(models.Model):
    review = models.ForeignKey(
        Reviews,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:25]
