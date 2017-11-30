"-"
from distutils.core import setup

setup(
    name='socialTracker',
    version='0.1.0',
    packages=['socialtracker'],
    install_requires=[
        'twitter', 'requests', 'arrow', 'backports.functools_lru_cache',
        'unidecode'])
