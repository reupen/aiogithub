from aiogithub.objects.base_object import BaseResponseObject


class Issue(BaseResponseObject):
    _url = 'repos/{repo[owner][login]}/{repo[name]}/issues/{number}'  # FIXME
    pass
