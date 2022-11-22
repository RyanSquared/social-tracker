"-"
from distutils.core import setup

setup(
    name='socialTracker',
    version='0.2.0',
    packages=['socialtracker'],
    install_requires=[
        'twitter', 'requests', 'backports.functools_lru_cache',
        'pillow==9.3.0', 'requests-oauthlib'])
