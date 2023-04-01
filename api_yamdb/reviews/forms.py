from django import forms

from reviews.models import (Categories,
                            Comments,
                            GenreTitle,
                            Genres,
                            Reviews,
                            Titles,
                            User)


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


class GenreTitleForm(forms.ModelForm):
    class Meta:
        model = GenreTitle
        fields = '__all__'


class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = '__all__'


class TitlesForm(forms.ModelForm):
    class Meta:
        model = Titles
        fields = '__all__'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
