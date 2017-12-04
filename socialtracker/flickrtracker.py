"Module for Flickr SocialTracker."
from socialtracker.base import SocialTracker
import requests_oauthlib
import arrow


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
            "https://api.flickr.com/services/rest", params=dict(params))
        content.raise_for_status()
        return content.json()

    def get_posts(self):
        """Yield posts from Flickr's API."""
        if self.flickr is None:
            self._setup_OAuth()
        # Hack to get around Flickr's 100-image results... Just use an iterator
        # that goes up to 30 "posts" and then kills the containing thread
        # by raising a StopIteration. Also, super ugly hack to get around
        # Python 2's range() returning a list.
        n = (x for x in range(30))  # pylint: disable=invalid-name
        # Limit to a week ago
        time = arrow.utcnow().shift(weeks=-1)
        for tag in self.tags:
            params = [("tags", tag),
                      ("extras", "date_upload,owner_name,tags,icon_server"),
                      ("min_upload_date", time.timestamp)]
            content = self._get_from_endpoint(
                "flickr.photos.search", params)
            for post in content["photos"]["photo"]:
                yield post
                next(n)

    @staticmethod
    def format_image_url(post):
        """Format a URL from a Flickr post."""
        data = [post["farm"], post["server"], post["id"], post["secret"]]
        return ("https://farm{}.staticflickr.com/{}/{}_{}_b.jpg").format(*data)

    @staticmethod
    def format_icon_url(post):
        """Format a URL for an icon from a Flickr post."""
        data = [post["iconfarm"], post["iconserver"], post["owner"]]
        return "http://farm{}.staticflickr.com/{}/buddyicons/{}.jpg".format(
            *data)
