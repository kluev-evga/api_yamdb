from api.permissions import IsOwnerOrIsAdmin
from api.serializers import (
    CategoriesSerializer,
    CommentsSerializer,
    ReviewsSerializer,
    GenresSerializer,
    SignupSerializer,
    TitlesSerializer,
    AuthSerializer,
)

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, mixins, status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from reviews.models import Categories, Comments, Genres, Reviews, Titles, User
from .permissions import AdminModeratorOwnerOrReadOnly


class GetListCreateDeleteViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, GenericViewSet
):
    pass


class SignupView(APIView):
    def send_confirmation_email(self, username, email):
        """File mailer - сохранить email в sent_mails"""
        user = User.objects.get(username=username, email=email)
        confirmation_code = default_token_generator.make_token(user)

        subject = 'Код для получения токена'
        body = (f'{"-" * 79}\n\nusername:\n{username}\n\n'
                f'Код подтверждения:\n{confirmation_code}\n')
        send_mail(
            subject,
            body,
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
        )

    def post(self, request):
        """Регистрация пользователя / получение confirmation code"""
        username = request.data.get('username', None)
        email = request.data.get('email', None)

        exist = User.objects.filter(username=username, email=email).exists()
        if not exist:
            serializer = SignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)  # stop here if no valid
            serializer.save()

        self.send_confirmation_email(username, email)

        return Response(request.data, status=status.HTTP_200_OK)


class AuthView(APIView):
    def post(self, request):
        """Получение JWT токена"""
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoriesViewSet(GetListCreateDeleteViewSet):
    """ViewSet for Categories endpoint"""
    serializer_class = CategoriesSerializer
    queryset = Categories.objects.all()
    permission_classes = (IsOwnerOrIsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(GetListCreateDeleteViewSet):
    serializer_class = GenresSerializer
    queryset = Genres.objects.all()
    permission_classes = (IsOwnerOrIsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(ModelViewSet):
    """ViewSet for Titles endpoint"""
    serializer_class = TitlesSerializer
    queryset = Titles.objects.all()
    permission_classes = (IsOwnerOrIsAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')


class UsersViewSet(ModelViewSet):
    pass


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [AdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get("title_id"))

        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (AdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(
            Reviews,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Reviews,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
