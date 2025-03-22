from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("", views.index, name="home"),
    path("home", views.index, name="home"),
    path('genre/<str:genre_name>/', views.genre_manga_view, name='genre_manga'),
    path("popular", views.popular_manga, name="popular"),
    path("action", views.action, name="action"),
    path("Contact", views.Contact, name="Contact"),
    path("about", views.about, name="about"),
    path("ongoing", views.ongoing, name="ongoing"),
    path("read", views.read, name="read"),
    path("login",views.login_user,name="login"),
    path("logout",views.logout_user,name="logout"),
    path("signup", views.signup_user,name="signup"),
    path('search/', views.search_manga, name='search_manga'),
    path('read/<str:genre>/<path:manga_title>/<int:chapter_number>/', views.read_manga, name='read_manga'),
    #path("api/get-chapter-images/", views.get_chapter_images_api, name="get_chapter_images_api"),
]