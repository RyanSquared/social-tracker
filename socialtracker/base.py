"Base class for socialTrackers."
import collections
import logging
import os
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
        if os.path.isfile(filename):
            logging.debug("Found old icon for: %s", filename)
            return filename
        for number, icon in enumerate(SocialTracker.icons):
            if icon[0] == url:
                # percolate up to implement priority
                if number > 1:
                    # but don't just cycle between the first two values
                    SocialTracker.icons.remove(icon)
                    SocialTracker.icons.appendleft(icon)
                image = icon[1]
                logging.debug("Found cached icon for: %s", filename)
                break
        else:
            logging.debug("Pulling from %s to get data for %s", url, filename)
            image = requests.get(url).content
            SocialTracker.icons.appendleft((url, image))
        with open(filename, "wb") as handler:
            handler.write(image)
        return filename

    @staticmethod
    def render_media(url, filename):
        """Pull media from `url` and place output in `filename`."""
        if os.path.isfile(filename):
            logging.debug("Found saved media for: %s", filename)
            return
        logging.debug("Opening stream for URL: %s", url)
        stream = requests.get(url, stream=True)
        with open(filename, 'wb') as handle:
            for block in stream.iter_content(1024):
                handle.write(block)
