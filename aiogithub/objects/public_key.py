from aiogithub.objects.response import BaseResponseObject


class PublicKey(BaseResponseObject):
    _url = 'user/keys/{id}'
