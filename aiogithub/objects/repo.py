from aiogithub.objects.base_object import BaseResponseObject

from aiogithub import objects


class Repo(BaseResponseObject):
    @staticmethod
    def _get_key_mappings():
        return {
            'owner': objects.User,
            'organization': objects.Organization,
            'parent': Repo,
            'source': Repo
        }
