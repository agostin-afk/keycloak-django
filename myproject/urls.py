
from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework import routers
from .views import UrlExempleView



urlpatterns = [
    path('admin/', admin.site.urls),
]

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns += [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('login/', CustomLoginView.as_view(), name='login'),
    path('urlExemple/', UrlExempleView, name='url-exemple'),
    
    # path('homeExemple/', HomeExempleView.as_view(), name='home-exemple'),
]