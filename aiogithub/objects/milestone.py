from aiogithub.objects.base_object import BaseResponseObject


class Milestone(BaseResponseObject):
    _url = 'repos/{user}/{repo}/milestones/{number}'
    pass
