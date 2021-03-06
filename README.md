# social-tracker
A social activity monitor. Uses Python threads.  Documentation is visible with
`pydoc2 <module>` or `pydoc3 <module>`.

Python 3 support is not guaranteed.

Because this library was designed for a program running on Raspberry Pis,
images rendered by the `render_icon()` or `render_media()` functions (which
should be either JPG or PNG format) will be converted to PNG, as PNG allows
for hardware decoding.

## Examples

```py
# pylint: disable=invalid-name
import arrow
from socialtracker import TrackerWatcher
from socialtracker.twittertracker import TwitterTracker

trackerwatcher = TrackerWatcher()
twitter = TwitterTracker({
    "consumer_key": "A9g3HedzSZBT6cFWr70sjd91F",
    "consumer_secret": "-",
    "auth_key": "2940219984-szoTUAx02RUtyKKZOLqtzrRxIMlycgewbZbcXat",
    "auth_secret": "-",
}, ["from:POTUS"])

trackerwatcher.attach_tracker(twitter, "twitter")

tweets = []


@trackerwatcher.handle_tracker("twitter")
def handle_twitter(post):
    "-"
    # TODO replace with datetime, don't use arrow
    date = arrow.get(post["created_at"], "ddd MMM DD HH:mm:ss Z YYYY")
    tweets.append({
        "time": date.format("hh:mm A"),
        "source": "twitter",
        "user": "@" + post["user"]["screen_name"],
        "text": post["text"],
        "id": post["id"],
        "icon": "::TODO::",  # Go read up on SocialTracker.render_icon()
    })


trackerwatcher.setup_watch().wait()

for tweet in tweets:
    print repr(tweet)
```
