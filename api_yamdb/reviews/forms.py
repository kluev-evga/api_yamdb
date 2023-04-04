from django import forms

from reviews.models import (
    Categories,
    Comments,
    Genres,
    Reviews,
    Titles,
    User
)


class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = '__all__'


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = '__all__'


class GenresForm(forms.ModelForm):
    class Meta:
        model = Genres
        fields = '__all__'


class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = '__all__'


class TitlesForm(forms.ModelForm):
    class Meta:
        model = Titles
        fields = [
            'id', 'name', 'year', 'description', 'category'
        ]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'role', 'bio', 'first_name', 'last_name'
        ]
