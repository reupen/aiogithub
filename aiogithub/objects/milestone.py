from aiogithub.objects.response import BaseResponseObject


class Milestone(BaseResponseObject):
    _url = 'repos/{login}/{repo}/milestones/{number}'
    pass
