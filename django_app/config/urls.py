from django.contrib import admin
from django.urls import path
from demo import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", views.login_keycloak, name="login"),
    path("callback/", views.oidc_callback, name="callback"),
    path("", views.home, name="home"),
    path("protegido/", views.protegido, name="protegido"),
    path("logout/", views.logout_view, name="logout"),
]
