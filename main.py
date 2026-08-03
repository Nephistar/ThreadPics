"""
ThreadPics
https://github.com/Nephistar/ThreadPics
License: GPL-3.0
Usage:
    main.py
    main.py --example
    main.py (-h | --help)
Options:
    --example       Run basic functionality with example files.
    -h --help       Show this screen.
"""


from docopt import docopt
from Control import Control


if __name__ == '__main__':
    args = docopt(__doc__)
    Control(args)


