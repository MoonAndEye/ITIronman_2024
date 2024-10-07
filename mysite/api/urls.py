from django.urls import path
from .views import hello_world, login_view

urlpatterns = [
    path('helloworld/', hello_world, name='hello_world'),
    path('login/', login_view, name='login'),
]
