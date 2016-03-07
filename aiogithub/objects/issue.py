from aiogithub.objects.base_object import BaseResponseObject


class Issue(BaseResponseObject):
    _url = 'repos/{user}/{repo}/issues/{number}'
    pass
