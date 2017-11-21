"Module for Instagram SocialTracker"
from socialtracker.base import SocialTracker
import requests

# Some notes:
# - Only one token is used
# \- Auth token is linked to client token
# - There's no application token used in HTTP requests
# - There's no decent Python module for this kind of thing. I should write one.


class InstagramTracker(SocialTracker):
    "Use Instagram's API to pull in requests."

    def __init__(self, settings, tags=None):
        """Set up data from `settings` and initialize tags."""
        super(InstagramTracker, self).__init__(tags)
        self.auth_token = settings["auth_token"]

    def _get_from_endpoint(self, endpoint, params=None):
        """Query the Instagram API and raise exceptions on bad requests."""
        if params is None:
            params = [('ACCESS_TOKEN', self.auth_token)]
        else:
            params.append([('ACCESS_TOKEN', self.auth_token)])

        content = requests.get(
            "https://api.instagram.com{}".format(endpoint), params)
        content.raise_for_status()
        return content.json()

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
        raise NotImplementedError("::TODO::")

    def get_posts(self):
        """Yield posts from Instagram's API"""
        for tag in self.tags:
            # Following a user, yield from user posts
            if tag[:5].lower() == "from:":
                for post in self._get_user_posts(tag[5:].strip()):
                    yield post
            else:
                tag = tag[1:] if tag[0] == "#" else tag
                for post in self._get_tagged_posts(tag):
                    yield post
