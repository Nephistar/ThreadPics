"""
ThreadPics
https://github.com/Nephistar/ThreadPics
License: GPL-3.0
Usage:
    main.py [<ref_file> <img_dir> <stats_file> <plot_dir>]
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

    # default paths
    args['<ref_file>'] = './tables/reference.csv'
    args['<img_dir>'] = './pics/'
    args['<stats_file>'] = './tables/stats.csv'
    args['<plot_dir>'] = './plots/'

    # example paths
    if args['--example']:
        args['<ref_file>'] = './example/tables/lord_libidan_hexcodes.csv'
        args['<img_dir>'] = './example/pics/'
        args['<stats_file>'] = './example/tables/stats.csv'
        args['<plot_dir>'] = './example/plots/'

    Control(args)


