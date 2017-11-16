"Base class for socialTrackers."


class SocialTracker(object):
    """Implementation class for all socialTrackers."""

    def __init__(self, tags=None):
        self.tags = tags if tags is not None else []

    def get_posts(self):
        """Return a generator to yield posts from an API."""
        raise NotImplementedError("base class", SocialTracker)

    def render_icon(self, post):
        """Create an icon from a post/URL and put it into a post"""
        raise NotImplementedError("base class", SocialTracker)
