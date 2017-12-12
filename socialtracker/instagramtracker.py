"Module for Instagram SocialTracker"
try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache
from socialtracker.base import SocialTracker
import requests

# Some notes:
# - Only one token is used
# \- Auth token is linked to client token
# - There's no application token used in HTTP requests
# - There's no decent Python module for this kind of thing. I should write one
# - Users are accessible only by ID, not username


class InstagramTracker(SocialTracker):
    "Use Instagram's API to pull in requests."

    def __init__(self, settings, tags=None):
        """Set up data from `settings` and initialize tags."""
        super(InstagramTracker, self).__init__(tags)
        self.auth_token = settings["auth_token"]
        self.client_id = settings["client_id"]

    def _get_from_endpoint(self, endpoint, params=None):
        """Query the Instagram API and raise exceptions on bad requests."""
        if params is None:
            params = [('access_token', self.auth_token),
                      ('client_id', self.client_id)]
        else:
            params.extend([('access_token', self.auth_token),
                           ('client_id', self.client_id)])

        content = requests.get(
            "https://api.instagram.com{}".format(endpoint), params)
        return content.json()

    @lru_cache()
    def _get_uid_from_username(self, username):
        "Get a user ID for usage with API from an Instagram username"
        data = self._get_from_endpoint("/v1/users/search", [("q", username)])
        return data["data"][0]["id"]

    def _get_tagged_posts(self, tag):
        """Get posts from a specific tag"""
        data = self._get_from_endpoint("/v1/tags/{}/media/recent".format(
            tag))["data"]
        for post in data:
            yield post

    def _get_user_posts(self, user):
        """Get posts from a specific user"""
        # Implementation consideration:
        # Instagram has lookup based off of ID, not username, so accounts
        # should be changed to an ID instead of a username.
        userid = self._get_uid_from_username(user)
        data = self._get_from_endpoint("/v1/users/{}/media/recent".format(
            userid))["data"]
        for post in data:
            yield post

    def get_posts(self):
        """Yield posts from Instagram's API"""
        for tag in self.tags:
            try:
                # Following a user, yield from user posts
                if tag[:5].lower() == "from:":
                    for post in self._get_user_posts(tag[5:].strip()):
                        yield post
                else:
                    tag = tag[1:] if tag[0] == "#" else tag
                    for post in self._get_tagged_posts(tag):
                        yield post
            except KeyError:  # If `data` doesn't exist (invalid request)
                pass
