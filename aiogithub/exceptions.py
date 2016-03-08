class GitHubException(Exception):
    pass


class FieldNotLoaded(GitHubException):
    pass


class HttpException(GitHubException):
    def __init__(self, status):
        self.status = status
