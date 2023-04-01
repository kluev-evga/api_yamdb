from api.views import (
    AuthView,
    CategoriesViewSet,
    GenresViewSet,
    SignupView,
    UsersViewSet
)

from django.urls import include, path

from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenresViewSet, basename='genres')

urlpatterns = [
    path('api/v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('api/v1/auth/token', AuthView.as_view(), name='auth'),
    path('api/v1/', include(router.urls)),
]
