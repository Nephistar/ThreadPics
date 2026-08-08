"""
ThreadPics
https://github.com/Nephistar/ThreadPics
License: GPL-3.0
Usage:
    main.py [<ref_file> <img_dir> <stats_file>]
    main.py --plot [--show --hue --lc (--set_window <lch_y_top>) <ref_file> <img_dir> <stats_file> <plot_dir>]
    main.py --example
    main.py (-h | --help)
Options:
    --plot          Also plot histograms of the results. (Statistics file will be saved anyway.)
                    Default is combined Oklch histograms drawn in a standard window for better comparison.
                    The top bound of the y-axis may be below the maximum, so peaks may be cut off.
    --show          Show the histogram(s) of the first thread after saving.
    --hue           Also draw histograms for hue only. Windows are set dynamically.
    --lc            Also draw combined histograms for lightness and chroma, without hue. Windows are set dynamically.
    --set_window    Define an integer number as a custom top bound of the y-axis in the combined Oklch histograms.
    --example       Run basic functionality with example files.
    -h --help       Show this screen.
"""


from docopt import docopt
from Control import Control


if __name__ == '__main__':
    args = docopt(__doc__)

    # default paths
    if args['<ref_file>'] is None:
        args['<ref_file>'] = './tables/reference.csv'
    if args['<img_dir>'] is None:
        args['<img_dir>'] = './pics/'
    if args['<stats_file>'] is None:
        args['<stats_file>'] = './tables/stats.csv'
    if args['<plot_dir>'] is None:
        args['<plot_dir>'] = './plots/'

    # example paths
    if args['--example']:
        args['<ref_file>'] = './example/tables/lord_libidan_hexcodes.csv'
        args['<img_dir>'] = './example/pics/'
        args['<stats_file>'] = './example/tables/stats.csv'
        args['<plot_dir>'] = './example/plots/'

    Control(args)


