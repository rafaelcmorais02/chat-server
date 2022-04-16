from email.mime import message
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def welcome(request):
    data = {
        'message' : 'Bem vindo a API user'
    }
    return Response(data, status=200)