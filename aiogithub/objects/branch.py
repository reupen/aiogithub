from aiogithub.objects.base_object import BaseResponseObject


class Branch(BaseResponseObject):
    _url = 'repos/{repo[owner][login]}/{repo[name]}/branches/{name}'  # FIXME
    pass
