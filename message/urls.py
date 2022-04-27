from django.urls import path
from .views import createMessageView, getMessagesView

urlpatterns = [
    path('/register', createMessageView),
    path('/all', getMessagesView)
]
