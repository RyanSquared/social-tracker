"Monitor social networks such as Twitter and Instagram."
import logging
import threading
import six
import json
from socialtracker.base import SocialTracker


class TrackerThread(threading.Thread):
    "Thread class for iterating over posts and using callbacks."
    def __init__(self, tracker):
        super(TrackerThread, self).__init__()
        self.tracker = tracker

    def log(self, *args):
        "Write a message to output"
        logging.info(" ".join((str(x) for x in args + (self.tracker,))))

    def run(self):
        try:
            post_cache = {}
            self.log("running", self)
            for post in self.tracker["tracker"].get_posts():
                _hash = hash(json.dumps(post, sort_keys=True))
                if post_cache.get(_hash) is not None:
                    continue
                else:
                    post_cache[_hash] = True
                for callback in self.tracker["handlers"]:
                    try:
                        callback(post)
                    except Exception as err:  # pylint: disable=broad-except
                        self.log("Callback had exception:", repr(callback),
                                 repr(err))
            self.log("dying", self)
        except Exception as err:  # pylint: disable=broad-except
            self.log("Exception in pulling posts:", repr(err))


class TrackerWatcher(object):
    "Handle callbacks for trackers."

    def __init__(self):
        self.trackers = {}

    def log(self, *args):
        "Write a message to output"
        logging.info(" ".join((str(x) for x in args + (self,))))

    def attach_tracker(self, tracker, name):
        "Add a value of `tracker` with given name `name`."
        if not isinstance(tracker, SocialTracker):
            raise TypeError("expected", SocialTracker, "got", type(tracker))
        self.trackers[name] = {
            "tracker": tracker,
            "handlers": [],
            "thread": None
        }

    def handle_tracker(self, name):
        "Add a callback to be processed when tracker of `name` gets a post,"
        def attach_tracker(callback):  # pylint: disable=missing-docstring
            self.trackers[name]["handlers"].append(callback)
        return attach_tracker

    def setup_watch(self):
        "Create and manage threads"
        for name, tracker in six.iteritems(self.trackers):
            thread = tracker.get("thread")
            if thread is None or not thread.isAlive():
                # Start a new thread
                self.log("starting thread:", name, tracker)
                tracker["thread"] = TrackerThread(tracker)
                tracker["thread"].start()
        return self

    def wait(self):
        "Wait for all currently-running threads to finish."
        for _, tracker in six.iteritems(self.trackers):
            tracker["thread"].join()
