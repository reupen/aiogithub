from aiogithub.objects.base_object import BaseResponseObject


class PublicKey(BaseResponseObject):
    _url = 'user/keys/{id}'
