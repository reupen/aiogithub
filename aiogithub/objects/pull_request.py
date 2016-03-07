from aiogithub.objects.base_object import BaseResponseObject


class PullRequest(BaseResponseObject):
    _url = 'repos/{user}/{repo}/pulls/{number}'
    pass
