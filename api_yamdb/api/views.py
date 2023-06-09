from api.permissions import (
    AdminModeratorOwnerOrReadOnly,
    AnyAuthorized,
    IsAdminUser,
    IsOwnerOrIsAdmin,
)
from api.serializers import (
    AuthSerializer,
    CategoriesSerializer,
    CommentsSerializer,
    GenresSerializer,
    ReviewsSerializer,
    SignupSerializer,
    TitlesSerializer,
    UserPatchSerializer,
    UserSerializer,
)

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import (
    CharFilter,
    DjangoFilterBackend,
    FilterSet,
)

from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from reviews.models import Categories, Genres, Review, Title, User


class GetListCreateDeleteViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, GenericViewSet
):
    pass


class SignupView(APIView):
    @staticmethod
    def get_confirmation_code(username, email):
        user = User.objects.get(username=username, email=email)
        return default_token_generator.make_token(user)

    def send_confirmation_email(self, username, email):
        """File mailer - save email into sent_mails"""
        confirmation_code = self.get_confirmation_code(username, email)

        subject = 'Код для получения токена'
        body = (f'{"-" * 79}\n\nusername:\n{username}\n\n'
                f'Код подтверждения:\n{confirmation_code}\n')
        mail_from = 'from@example.com'
        mail_to = [email, ]

        send_mail(subject, body, mail_from, mail_to, fail_silently=False)

    def post(self, request):
        """Register new user / get confirmation code"""
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


class TitleFilter(FilterSet):
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre')


class TitlesViewSet(ModelViewSet):
    """ViewSet for Titles endpoint"""
    serializer_class = TitlesSerializer
    queryset = Title.objects.all()
    permission_classes = (IsOwnerOrIsAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = (AdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))

        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (AdminModeratorOwnerOrReadOnly, )

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "username"
    search_fields = ('username',)
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    ]


class UsersMeView(APIView):
    permission_classes = (AnyAuthorized,)

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=request.user.username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=request.user.username)
        serializer = UserPatchSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
