"Module for Twitter SocialTracker."
from socialtracker.base import SocialTracker
import twitter

htmlparser = HTMLParser()  # pylint: disable=invalid-name


class TwitterTracker(SocialTracker):
    "Use Twitter's API to pull in requests."

    def __init__(self, settings, tags=None):
        """Set up data from `settings` and initialize tags."""
        super(TwitterTracker, self).__init__(tags)
        self.auth_key = settings["auth_key"]
        self.auth_secret = settings["auth_secret"]
        self.consumer_key = settings["consumer_key"]
        self.consumer_secret = settings["consumer_secret"]
        self.tweet_count = settings.get("count") or 30
        self.twitter = None

    def _setup_OAuth(self):  # pylint: disable=invalid-name
        """Set up a `twitter` object with OAuth data."""
        self.twitter = twitter.Twitter(auth=twitter.OAuth(
            self.auth_key, self.auth_secret,
            self.consumer_key, self.consumer_secret))

    def get_posts(self):
        """Yield posts from Twitter's API."""
        if self.twitter is None:
            self._setup_OAuth()
        for tag in self.tags:
            for tweet in self.twitter.search.tweets(
                    q=tag,
                    count=self.tweet_count, result_type="recent")["statuses"]:
                yield tweet
