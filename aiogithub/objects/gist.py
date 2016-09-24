from aiogithub.objects.response import BaseResponseObject


class Gist(BaseResponseObject):
    _url = 'gists/{id}'
    pass
