from django.urls import path
from .views import welcome, userRegisterView, userListView
from .auth.authTokenView import CustomAuthToken
urlpatterns = [
    path('', welcome),
    path('/register', userRegisterView),
    path('/token', CustomAuthToken.as_view()),
    path('/all', userListView)
]
