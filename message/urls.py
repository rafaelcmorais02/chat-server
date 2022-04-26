from django.urls import path
from .views import createMessageView

urlpatterns = [
    path('/register', createMessageView),
]
