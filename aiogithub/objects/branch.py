from aiogithub import objects
from aiogithub.objects.response import BaseResponseObject
from aiogithub.utils import return_key


class Branch(BaseResponseObject):
    _url = 'repos/{login}/{repo}/branches/{branch}'

    @staticmethod
    def _get_key_mappings():
        return {
            'commit': objects.Commit
        }

    @property
    @return_key
    def name(self) -> str:
        pass

    @property
    @return_key
    def commit(self) -> 'objects.Commit':
        pass

    @property
    def links(self) -> dict:
        return self.get('_links')
