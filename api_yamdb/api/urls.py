from django.urls import path, include
from rest_framework import routers

from .views import (
    UsersViewSet,
    SignupView,
    AuthView
)

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('api/v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('api/v1/auth/token', AuthView.as_view(), name='auth'),
    path('api/v1/', include(router.urls)),
]
