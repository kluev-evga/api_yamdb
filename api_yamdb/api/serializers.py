from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from reviews.models import Titles, Comments, Reviews, Categories, Genres, User

JWT = TokenObtainPairSerializer()


class AuthSerializer(serializers.Serializer):
    """Get JWT token, auth/token serializer"""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def to_representation(self, user):
        """POST response view, return JWT token"""
        token = str(JWT.get_token(user).access_token)
        return {'token': token}

    def validate(self, data):
        username = data.get('username', None)
        confirmation_code = data.get('confirmation_code', None)

        user = get_object_or_404(User, username=username)
        # Проверка confirmation_code:
        valid = default_token_generator.check_token(user, confirmation_code)
        if not valid:
            raise serializers.ValidationError(
                'Некорректный код подтверждения и/или username'
            )

        return user  # вернул user чтобы получить его в to_representation()


class SignupSerializer(serializers.ModelSerializer):
    """auth/signup serializer"""
    class Meta:
        model = User
        fields = ('username', 'email',)


class ReviewsSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError('10-бальная шкала оценки.')
        return

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        if request.method == 'POST':
            if Reviews.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError('Не более одного отзыва'
                                                  'на пользователя')
        return data

    class Meta:
        model = Reviews
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field='text'
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comments
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    """Serializer for Categories endpoint"""
    class Meta:
        model = Categories
        fields = ('name', 'slug',)


class GenresSerializer(serializers.ModelSerializer):
    """Serializer for Genres endpoint"""
    class Meta:
        model = Genres
        fields = ('name', 'slug',)


class UserSerializer(serializers.ModelSerializer):
    """users/* serializer"""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class UserPatchSerializer(serializers.ModelSerializer):
    """users/me PATCH serializer"""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',)
