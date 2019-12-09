from django.urls import path
from . import views

# name attr is used to be able to refer to this url by it's name
# from templates if you wish:
# <a href="{% url 'app_name.url_name' %}">Display Text</a>
# using the anchor tag like this makes it so if you change the url you don't
# have to also change the anchor tag
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('home', views.home, name="home"),
    path('register', views.register, name="register"),
    path('users/<int:id>', views.users_profile, name="users_profile"),

    path('shirts/new', views.new_shirt, name="new_shirt"),
    path('shirts/create', views.create_shirt, name="create_shirt"),
    path('shirts/<int:shirt_id>/like', views.like_shirt, name="like_shirt"),

    path('shirts', views.all_shirts, name="all_shirts"),
]
