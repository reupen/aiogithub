from aiogithub.objects.base_object import BaseResponseObject

from aiogithub import objects


class Repo(BaseResponseObject):
    default_urls = {
        "archive_url": "repos/{owner[login]}/{name}/{{archive_format}}{{/ref}}",
        "assignees_url": "repos/{owner[login]}/{name}/assignees{{/user}}",
        "blobs_url": "repos/{owner[login]}/{name}/git/blobs{{/sha}}",
        "branches_url": "repos/{owner[login]}/{name}/branches{{/branch}}",
        "collaborators_url": "repos/{owner[login]}/{name}/collaborators{{/collaborator}}",
        "comments_url": "repos/{owner[login]}/{name}/comments{{/number}}",
        "commits_url": "repos/{owner[login]}/{name}/commits{{/sha}}",
        "compare_url": "repos/{owner[login]}/{name}/compare/{{base}}...{{head}}",
        "contents_url": "repos/{owner[login]}/{name}/contents/{{+path}}",
        "contributors_url": "repos/{owner[login]}/{name}/contributors",
        "deployments_url": "repos/{owner[login]}/{name}/deployments",
        "downloads_url": "repos/{owner[login]}/{name}/downloads",
        "events_url": "repos/{owner[login]}/{name}/events",
        "forks_url": "repos/{owner[login]}/{name}/forks",
        "git_commits_url": "repos/{owner[login]}/{name}/git/commits{{/sha}}",
        "git_refs_url": "repos/{owner[login]}/{name}/git/refs{{/sha}}",
        "git_tags_url": "repos/{owner[login]}/{name}/git/tags{{/sha}}",
        "git_url": "git:github.com/octocat/Hello-World.git",
        "hooks_url": "repos/{owner[login]}/{name}/hooks",
        "issue_comment_url": "repos/{owner[login]}/{name}/issues/comments{{/number}}",
        "issue_events_url": "repos/{owner[login]}/{name}/issues/events{{/number}}",
        "issues_url": "repos/{owner[login]}/{name}/issues{{/number}}",
        "keys_url": "repos/{owner[login]}/{name}/keys{{/key_id}}",
        "labels_url": "repos/{owner[login]}/{name}/labels{{/name}}",
        "languages_url": "repos/{owner[login]}/{name}/languages",
        "merges_url": "repos/{owner[login]}/{name}/merges",
        "milestones_url": "repos/{owner[login]}/{name}/milestones{{/number}}",
        "notifications_url": "repos/{owner[login]}/{name}/notifications{{?since, all, participating}}",
        "pulls_url": "repos/{owner[login]}/{name}/pulls{{/number}}",
        "releases_url": "repos/{owner[login]}/{name}/releases{{/id}}",
        "stargazers_url": "repos/{owner[login]}/{name}/stargazers",
        "statuses_url": "repos/{owner[login]}/{name}/statuses/{{sha}}",
        "subscribers_url": "repos/{owner[login]}/{name}/subscribers",
        "subscription_url": "repos/{owner[login]}/{name}/subscription",
        "tags_url": "repos/{owner[login]}/{name}/tags",
        "teams_url": "repos/{owner[login]}/{name}/teams",
        "trees_url": "repos/{owner[login]}/{name}/git/trees{{/sha}}"
    }

    @staticmethod
    def _get_key_mappings():
        return {
            'owner': objects.User,
            'organization': objects.Organization,
            'parent': Repo,
            'source': Repo
        }

    async def get_assignees(self):
        return await self._get_related_url('assignees_url', objects.User)

    async def get_blobs(self):
        return await self._get_related_url('blobs_url',
                                           objects.BaseResponseObject)

    async def get_branches(self):
        return await self._get_related_url('branches_url', objects.Branch)

    async def get_collaborators(self):
        return await self._get_related_url('collaborators_url', objects.User)

    async def get_comments(self):
        return await self._get_related_url('comments_url',
                                           objects.BaseResponseObject)

    async def get_commits(self):
        return await self._get_related_url('commits_url',
                                           objects.BaseResponseObject)

    # compare, contents

    async def get_contributors(self):
        return await self._get_related_url('contributors_url', objects.User)

    async def get_events(self):
        return await self._get_related_url('events_url', objects.Event)

    async def get_forks(self):
        return await self._get_related_url('forks_url', objects.Repo)

    async def get_issues(self):
        return await self._get_related_url('issues_url',
                                           objects.BaseResponseObject)

    async def get_stargazers(self):
        return await self._get_related_url('stargazers_url', objects.User)
