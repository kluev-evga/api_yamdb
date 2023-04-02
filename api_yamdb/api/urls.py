from django.urls import path, include
from rest_framework import routers

from .views import (
    UsersViewSet,
    SignupView,
    AuthView,
    CommentsViewSet,
    ReviewsViewSet,
)

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewsViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentsViewSet, basename='comments')

urlpatterns = [
    path('api/v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('api/v1/auth/token', AuthView.as_view(), name='auth'),
    path('api/v1/', include(router.urls)),
]
