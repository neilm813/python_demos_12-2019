from django.urls import path
from . import views

# NO LEADING SLASHES
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('home', views.home, name='home'),
    path('logout', views.logout, name='logout'),

    # doggos
    path('doggos/new', views.doggo_new, name='doggo_new'),
    path('doggos/create', views.doggo_create, name='doggo_create'),
    path('doggos/<int:doggo_id>', views.doggo_profile, name='doggo_profile'),
    path('doggos', views.doggos, name='doggos'),
    path('doggos/<int:doggo_id>/good_boy', views.good_boy, name='good_boy'),
]
