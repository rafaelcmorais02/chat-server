from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserListSerializer, UserRegisterSerializer
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from user.auth.authentication import BearerTokenAuthentication
from .services import UserServices


@api_view(['GET'])
def welcome(request):
    data = {
        'message': 'Bem vindo a API user'
    }
    return Response(data, status=200)


@api_view(['GET'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def userListView(request):
    users = CustomUser.objects.all()
    users_serializer = UserListSerializer(users, many=True)
    resp = {
        'data': UserServices.returnAllUser(users_serializer.data, request.user.id)
    }
    return Response(resp, status=200)


@api_view(['POST'])
def userRegisterView(request):
    user_serializer = UserRegisterSerializer(data=request.data)
    if user_serializer.is_valid():
        user_serializer.save()
        resp = {
            'message': 'usuário cadastrado com sucesso',
            'data': request.data
        }
        return Response(resp, status=201)
    else:
        return Response({'message': 'erro no cadastro do usuário'}, status=400)
