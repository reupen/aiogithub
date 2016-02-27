import re


def strip_github_url_params(url):
    return re.sub(r'{[^}]*}', '', url)
