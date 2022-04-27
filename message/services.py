from rest_framework.exceptions import APIException


class MessageServices:
    @staticmethod
    def returnMessageWithUserSender(request):
        data = request.data
        id = request.user.id
        data['user_sender'] = id
        return data

    @staticmethod
    def returnAllMessages(messages, id):
        new_messages = []
        for message in messages:
            if message['user_sender'] == id:
                new_messages.append(message)
        return new_messages
