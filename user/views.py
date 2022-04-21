from .serializers import UserRegisterSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def welcome(request):
    data = {
        'message': 'Bem vindo a API user'
    }
    return Response(data, status=200)


@api_view(['POST'])
def userRegisterView(request):
    user_serializer = UserRegisterSerializer(data=request.data)
    if user_serializer.is_valid():
        print('teste')
        user_serializer.save()
        resp = {
            'message': 'usuário cadastrado com sucesso',
            'data': request.data
        }
        return Response(resp, status=201)
    else:
        return Response({'message': 'erro no cadastro do usuário'}, status=400)
