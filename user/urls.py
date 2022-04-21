from django.urls import path
from .views import welcome, userRegisterView
urlpatterns = [
    path('', welcome),
    path('/register', userRegisterView),
]
