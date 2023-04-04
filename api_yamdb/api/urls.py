from api.views import (
    AuthView,
    CategoriesViewSet,
    GenresViewSet,
    SignupView,
    UsersViewSet,
    CommentsViewSet,
    ReviewsViewSet,
    UsersMeView,
)

from django.urls import include, path

from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenresViewSet, basename='genres')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewsViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentsViewSet, basename='comments')

urlpatterns = [
    path('api/v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('api/v1/auth/token/', AuthView.as_view(), name='auth'),
    path('api/v1/users/me/', UsersMeView.as_view(), name='users-self'),
    path('api/v1/', include(router.urls)),
]
