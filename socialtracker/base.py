"Base class for socialTrackers."
import collections
import io
import logging
import os
import time
import requests
from PIL import Image


class SocialTracker(object):
    """Implementation class for all socialTrackers."""

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
        filename = filename.rpartition(".")[0] + ".png"
        if os.path.isfile(filename):
            timestamp = time.time()
            os.utime(filename, (timestamp, timestamp))
            logging.debug("Found old icon for: %s", filename)
            return filename
        logging.debug("Pulling from %s to get data for %s", url, filename)
        content = requests.get(url).content
        image = Image.open(io.BytesIO(content))
        image.save(filename, "PNG")
        return filename

    @staticmethod
    def render_media(url, filename):
        """Pull media from `url` and place output in `filename`."""
        filename = filename.rpartition(".")[0] + ".png"
        if os.path.isfile(filename):
            timestamp = time.time()
            os.utime(filename, (timestamp, timestamp))
            logging.debug("Found saved media for: %s", filename)
            return filename
        logging.debug("Opening stream for URL: %s", url)
        ext = filename.rpartition(".")[2]
        if ext == "png" or ext == "jpg":
            content = requests.get(url).content
            image = Image.open(io.BytesIO(content))
            image.save(filename, "PNG")
            return filename
        stream = requests.get(url, stream=True)
        with open(filename, 'wb') as handle:
            for block in stream.iter_content(1024):
                handle.write(block)
        return filename
