from aiogithub.objects.base_object import BaseResponseObject


class Milestone(BaseResponseObject):
    _url = 'repos/{login}/{repo}/milestones/{number}'
    pass
