from aiogithub.objects.base_object import BaseResponseObject


class PullRequest(BaseResponseObject):
    _url = 'repos/{head[repo][owner][login]}/{head[repo][name]}/pulls/{number}'
    pass
