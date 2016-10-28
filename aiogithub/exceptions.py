class GitHubException(Exception):
    pass


class FieldNotLoaded(GitHubException):
    pass


class HttpException(GitHubException):
    def __init__(self, status, url):
        self.status = status
        self.url = url
