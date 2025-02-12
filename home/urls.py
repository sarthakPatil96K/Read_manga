from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("", views.index, name="home"),
    path("home", views.index, name="home"),
    path("popular", views.popular, name="popular"),
    path("action", views.action, name="action"),
    path("Contact", views.Contact, name="Contact"),
    path("about", views.about, name="about"),
    path("ongoing", views.ongoing, name="ongoing"),
    path("read", views.read, name="read"),
]