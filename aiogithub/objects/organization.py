from aiogithub.objects.base_object import BaseResponseObject


class Organization(BaseResponseObject):
    _url = 'orgs/{user}'
