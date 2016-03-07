from aiogithub.objects.base_object import BaseResponseObject


class Branch(BaseResponseObject):
    _url = 'repos/{user}/{repo}/branches/{number}'
    pass
