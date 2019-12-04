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
]
