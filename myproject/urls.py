from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers
from api_user.views import UserRegistrationView, user_login, user_logout
router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('api/', include(router.urls)),
    re_path(r'^keycloak/', include('django_keycloak.urls')),
]