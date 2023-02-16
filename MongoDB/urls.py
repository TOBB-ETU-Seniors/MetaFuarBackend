from django.urls import path

from . import views

urlpatterns = [path('account',views.account,name='account'),
               path("isUsernameAvailable", views.isUsernameAvailable, name="isUsernameAvailable"),
               path("create_lobby", views.create_lobby, name="create_lobby"),
               path("delete_lobby", views.delete_lobby, name="delete_lobby"),
               path("join_lobby", views.join_lobby, name="join_lobby"),
               path("exit_lobby", views.exit_lobby, name="exit_lobby")]