from aiogithub.objects.base_object import BaseResponseObject


class Gist(BaseResponseObject):
    _url = 'gists/{id}'
    pass
