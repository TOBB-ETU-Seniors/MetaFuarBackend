from django.urls import path

from . import views

urlpatterns = [path('account',views.account,name='account'),
               path("isUsernameAvailable/", views.isUsernameAvailable, name="isUsernameAvailable")]