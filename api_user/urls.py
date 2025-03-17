from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationView, user_login,user_logout

router = DefaultRouter()
router.register(r'register', UserRegistrationView.as_view(), name='register')

urlpatterns = [
    path('', include(router.urls)),
]