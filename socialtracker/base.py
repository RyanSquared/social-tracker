"Base class for socialTrackers."
import collections
import requests


class SocialTracker(object):
    """Implementation class for all socialTrackers."""
    # Store the last 5 icons downloaded
    icons = collections.deque(maxlen=5)

    def __init__(self, tags=None):
        self.posts_cache = []
        self.tags = tags if tags is not None else []

    def get_posts(self):
        """Return a generator to yield posts from an API."""
        raise NotImplementedError("base class", SocialTracker)

    @staticmethod
    def extend_icon_cache(length):
        "Extend the length of the icon cache (default 5 icons)."
        old_icons = SocialTracker.icons
        SocialTracker.icons = collections.deque(maxlen=length)
        SocialTracker.icons.extendleft(old_icons)

    @staticmethod
    def render_icon(url, filename):
        """Pull an icon from `url` and place the output in `filename`."""
        for number, icon in enumerate(SocialTracker.icons):
            if icon[0] == url:
                # percolate up to implement priority
                if number > 1:
                    # but don't just cycle between the first two values
                    SocialTracker.icons.remove(icon)
                    SocialTracker.icons.appendleft(icon)
                image = icon[1]
                break
        else:
            image = requests.get(url).content
            SocialTracker.icons.appendleft((url, image))
        with open(filename, "wb") as handler:
            handler.write(image)
        return filename
