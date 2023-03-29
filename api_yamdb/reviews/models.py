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
