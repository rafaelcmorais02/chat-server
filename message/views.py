from rest_framework.decorators import api_view, authentication_classes, permission_classes
from user.auth.authentication import BearerTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import MessageSerializer
from rest_framework.response import Response
from .services import MessageServices


@api_view(['Post'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def createMessageView(request):
    data = MessageServices.returnMessageWithUserSender(request)
    message_serializer = MessageSerializer(data=data)
    if message_serializer.is_valid():
        message_serializer.save()
        resp = {
            'message': 'mensagem registrada com sucesso',
            'data': request.data
        }
        return Response(resp, status=201)
    return Response({'message': 'erro no cadastro da mensagem'}, status=400)
