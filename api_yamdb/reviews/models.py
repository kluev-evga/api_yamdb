from django.db import models


class Categories(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
    )

    def __str__(self):
        return self.name


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

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name
