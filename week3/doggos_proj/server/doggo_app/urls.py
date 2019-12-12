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
    path('doggos/<int:doggo_id>/edit', views.doggo_edit, name='doggo_edit'),
    path('doggos/<int:doggo_id>/update',
         views.doggo_update, name='doggo_update'),
    path('doggos', views.doggos, name='doggos'),
    path('doggos/<int:doggo_id>/toggle_good_boy',
         views.doggo_toggle_good_boy, name='doggo_toggle_good_boy'),
    path('doggos/<int:doggo_id>/delete',
         views.doggo_delete, name='doggo_delete'),
]
