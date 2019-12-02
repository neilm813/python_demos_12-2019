from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('guest/<str:name>', views.guest, name='guest_page'),
    path('new', views.new, name='new')
]
