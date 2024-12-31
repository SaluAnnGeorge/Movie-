from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    
    path("", views.index, name="index"),
    path("movie_details/<int:id>/", views.movie_details, name="movie_details"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    

]