import keyword
from rest_framework.authentication import TokenAuthentication


class BearerTokemAuthentication(TokenAuthentication):
    keyword = 'Bearer'
