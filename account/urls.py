from django.urls import path
from . import views


urlpatterns = [
    path("logout/", views.logout, name="account_logout"),
    path("register/", views.register, name="account_register"),
    path("login/", views.login, name="account_login"),
    path("index/", views.index, name="index"),
]