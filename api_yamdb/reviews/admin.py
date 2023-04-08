from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Categories, Genres, Title, User, Review, Comments


@admin.register(User)
class UsersAdmin(UserAdmin):
    list_display = (
        'id', 'username', 'role', 'first_name', 'last_name', 'email', 'bio'
    )
    list_filter = ('role',)
    save_on_top = True
    save_as = True


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'slug'
    )
    search_fields = ('name',)


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'slug'
    )
    search_fields = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'year', 'description',
    )
    list_filter = ('year',)
    search_fields = ('name',)
    empty_value_display = '-empty-'


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'title', 'text', 'author', 'score', 'pub_date'
    )
    list_filter = ('pub_date',)
    search_fields = ('title', 'author',)


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'review', 'text', 'author', 'pub_date'
    )
    list_filter = ('pub_date',)
    search_fields = ('review', 'author',)
