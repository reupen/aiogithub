from aiogithub.objects.base_object import BaseResponseObject

from . import User, Organization


class Repo(BaseResponseObject):
    @staticmethod
    def _get_key_mappings():
        return {
            'owner': User,
            'organization': Organization,
            'parent': Repo,
            'source': Repo
        }
