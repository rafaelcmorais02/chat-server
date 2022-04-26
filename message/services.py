from rest_framework.exceptions import APIException


class MessageServices:
    @staticmethod
    def returnMessageWithUserSender(request):
        data = request.data
        id = request.user.id
        data['user_sender'] = id
        return data
