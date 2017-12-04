"Module for Flickr SocialTracker."
from socialtracker.base import SocialTracker
import requests_oauthlib


class FlickrTracker(SocialTracker):
    "Use Flickr's API to pull in requests."

    def __init__(self, settings, tags=None):
        """Set up data from `settings` and initialize tags."""
        super(FlickrTracker, self).__init__(tags)
        self.auth_key = settings["auth_key"]
        self.auth_secret = settings["auth_secret"]
        self.consumer_key = settings["consumer_key"]
        self.consumer_secret = settings["consumer_secret"]
        self.tweet_count = settings.get("count") or 30
        self.flickr = None

    def _setup_OAuth(self):  # pylint: disable=invalid-name
        """Set up a `flickr` object with OAuth data."""
        self.flickr = requests_oauthlib.OAuth1Session(
            self.consumer_key, client_secret=self.consumer_secret,
            resource_owner_key=self.auth_key,
            resource_owner_secret=self.auth_secret)

    def _get_from_endpoint(self, endpoint, params=None):
        """Query the endpoint"""
        if self.flickr is None:
            self._setup_OAuth()
        if params is None:
            params = [("method", endpoint)]
        else:
            params.insert(0, ("method", endpoint))
        params.append(("format", "json"))
        params.append(("nojsoncallback", "1"))
        content = self.flickr.get(
            "https://api.flickr.com/services/rest")
        print(content)

    def get_posts(self):
        """Yield posts from Flickr's API."""
        if self.flickr is None:
            self._setup_OAuth()
        for tag in self.tags:
            self._get_from_endpoint("flickr.photos.search", ["tags", "hi"])
