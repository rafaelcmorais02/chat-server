from django.urls import path
from .views import welcome, userRegisterView
from .auth.authTokenView import CustomAuthToken
urlpatterns = [
    path('', welcome),
    path('/register', userRegisterView),
    path('/token', CustomAuthToken.as_view())
]
