from matplotlib import pyplot as plt
import numpy as np

from ThreadPic import ThreadPic
from OklchConverter import Datum, Histogram


class OklchPlotter:
    def __init__(self, thread_pic: ThreadPic, reference: Datum=None):
        self.thread_pic = thread_pic
        if reference is None:
            self.ref_lightness = None
            self.ref_chroma = None
            self.ref_hue = None
        else:
            self.ref_lightness = reference.lightness_for_hist
            self.ref_chroma = reference.chroma_for_hist
            self.ref_hue = reference.hue_for_hist
        self.lightness_stats = Plot_Stats(thread_pic.oklch, self.ref_lightness, 'l')
        self.chroma_stats = Plot_Stats(thread_pic.oklch, self.ref_chroma, 'c')
        self.hue_stats = Plot_Stats(thread_pic.oklch, self.ref_hue,'h')
        self.x = None
        self.fig: plt.Figure
        self.ax: plt.Axes
        self.marker = ''

    def label_axes(self):
        self.ax.set_xlabel('value: L in 3‰, C in 1‰, H in 1° steps')
        self.ax.set_ylabel('pixel count')
        result = self.thread_pic.thread_id
        self.ax.set_title(result)
        print(result)

    def save(self, dir):
        path = dir + 'plot_' + self.thread_pic.thread_id + '_' + self.marker + '.png'
        plt.savefig(path)

    def show(self):
        plt.show()

    def close(self):
        plt.close()

    def plot_lightness(self):
        width = self.thread_pic.oklch.upper_limit_lightness + 1
        self.x = np.arange(width)
        self.fig, self.ax = plt.subplots()
        self.label_axes()
        yellow = Plot_Lines(self.x, self.ax, self.lightness_stats, 'y')
        self.ax.legend((yellow.line, yellow.triangle, yellow.dot,
                        yellow.dotted_vline_left, yellow.ref_vline),
                  ('lightness', 'median', 'mean',
                   'std dev', 'reference'))
        self.marker = 'l'

    def plot_chroma(self):
        width = self.thread_pic.oklch.upper_limit_chroma + 1
        self.x = np.arange(width)
        self.fig, self.ax = plt.subplots()
        self.label_axes()
        cyan = Plot_Lines(self.x, self.ax, self.chroma_stats, 'c')
        self.ax.legend((cyan.line, cyan.triangle, cyan.dot,
                        cyan.dotted_vline_left, cyan.ref_vline),
                       ('chroma', 'median', 'mean',
                        'std dev', 'reference'))
        self.marker = 'c'

    def plot_hue(self):
        width = self.thread_pic.oklch.upper_limit_hue + 1
        self.x = np.arange(width)
        self.fig, self.ax = plt.subplots()
        self.label_axes()
        magenta = Plot_Lines(self.x, self.ax, self.hue_stats, 'm')
        self.ax.legend((magenta.line, magenta.triangle, magenta.dot,
                        magenta.dotted_vline_left, magenta.ref_vline),
                       ('hue', 'median', 'mean',
                        'std dev', 'reference'))
        self.marker = 'h'

    def plot_combo_lc(self):
        # When combining the functions, we correct for the differing domains. Chroma is the widest.
        width = self.thread_pic.oklch.upper_limit_chroma + 1
        while len(self.lightness_stats.hist) < width:
            self.lightness_stats.hist.append(0)
        self.x = np.arange(width)
        self.fig, self.ax = plt.subplots()
        self.label_axes()
        cyan = Plot_Lines(self.x, self.ax, self.chroma_stats, 'c')
        yellow = Plot_Lines(self.x, self.ax, self.lightness_stats, 'y')
        self.ax.legend((yellow.line, cyan.line, cyan.triangle, cyan.dot,
                        cyan.dotted_vline_left, cyan.ref_vline),
                       ('lightness', 'chroma', 'median', 'mean',
                        'std dev', 'reference'))
        self.marker = 'lc'

    def plot_combo_lch(self, y_top: int):
        # When combining the functions, we correct for the differing domains. Chroma is the widest.
        width = self.thread_pic.oklch.upper_limit_chroma + 1
        while len(self.lightness_stats.hist) < width:
            self.lightness_stats.hist.append(0)
        while len(self.hue_stats.hist) < width:
            self.hue_stats.hist.append(0)
        self.x = np.arange(width)
        self.fig, self.ax = plt.subplots()
        self.ax.set_ylim(top=y_top)
        self.label_axes()
        magenta = Plot_Lines(self.x, self.ax, self.hue_stats, 'm')
        cyan = Plot_Lines(self.x, self.ax, self.chroma_stats, 'c')
        yellow = Plot_Lines(self.x, self.ax, self.lightness_stats, 'y')
        self.ax.legend((yellow.line, cyan.line, magenta.line,
                        magenta.triangle, magenta.dot,
                        magenta.dotted_vline_left, magenta.ref_vline),
                       ('lightness', 'chroma', 'hue',
                        'median', 'mean',
                        'std dev', 'reference'))
        self.marker = 'lch'


class Plot_Stats:
    def __init__(self, oklch: Histogram, reference, switch: str):
        if switch == 'l' or switch == 'c' or switch == 'h':
            self.switch = switch
        else:
            print('Invalid switch mode of Oklch Plotter Stats: ' + switch + ' - Needs to be either l, c or h.')
            return
        self.switch = switch
        self.ref = reference
        if self.switch == 'l':
            self.hist = oklch.hist_lightness.copy()
            self.mode = oklch.mode_lightness
            self.median = oklch.median_lightness
            self.mean = oklch.mean_lightness
            self.stdev = oklch.standard_deviation_lightness
            self.stdev_left = oklch.stdev_left_lightness
            self.stdev_right = oklch.stdev_right_lightness
            self.mode_val = oklch.mode_lightness_val
            self.median_val = oklch.median_lightness_val
            self.mean_val = oklch.mean_lightness_val
        elif self.switch == 'c':
            self.hist = oklch.hist_chroma.copy()
            self.mode = oklch.mode_chroma
            self.median = oklch.median_chroma
            self.mean = oklch.mean_chroma
            self.stdev = oklch.standard_deviation_chroma
            self.stdev_left = oklch.stdev_left_chroma
            self.stdev_right = oklch.stdev_right_chroma
            self.mode_val = oklch.mode_chroma_val
            self.median_val = oklch.median_chroma_val
            self.mean_val = oklch.mean_chroma_val
        elif self.switch == 'h':
            self.hist = oklch.hist_hue.copy()
            self.mode = oklch.mode_hue
            self.median = oklch.median_hue
            self.mean = oklch.mean_hue
            self.stdev = oklch.standard_deviation_hue
            self.stdev_left = oklch.stdev_left_hue
            self.stdev_right = oklch.stdev_right_hue
            self.mode_val = oklch.mode_hue_val
            self.median_val = oklch.median_hue_val
            self.mean_val = oklch.mean_hue_val

class Plot_Lines:
    def __init__(self, x, ax: plt.Axes, stats: Plot_Stats, mode: str):
        self.stats = stats
        if mode == 'y' or mode == 'c' or mode == 'm':
            self.mode = mode
        else:
            print('Invalid mode of Oklch Plotter Stats: ' + mode + ' - Needs to be either y, c or m.')
            return
        self.mode = mode
        if self.mode == 'y':
            self.ref_vline = ax.axvline(stats.ref, color='gold', linestyle='--')
            self.line, = ax.plot(x, stats.hist, color='yellow')
            self.triangle, = ax.plot(stats.median, stats.median_val, marker='v', color='gold')
            self.dot, = ax.plot(stats.mean, stats.mean_val, marker='o', color='gold')
            self.dotted_vline_left = ax.axvline(stats.stdev_left, color='yellow', linestyle=':')
            self.dotted_vline_right = ax.axvline(stats.stdev_right, color='yellow', linestyle=':')
        if self.mode == 'c':
            self.ref_vline = ax.axvline(stats.ref, color='chartreuse', linestyle='--')
            self.line, = ax.plot(x, stats.hist, color='cyan')
            self.triangle, = ax.plot(stats.median, stats.median_val, marker='v', color='chartreuse')
            self.dot, = ax.plot(stats.mean, stats.mean_val, marker='o', color='chartreuse')
            self.dotted_vline_left = ax.axvline(stats.stdev_left, color='cyan', linestyle=':')
            self.dotted_vline_right = ax.axvline(stats.stdev_right, color='cyan', linestyle=':')
        if self.mode == 'm':
            self.ref_vline = ax.axvline(stats.ref, color='crimson', linestyle='--')
            self.line, = ax.plot(x, stats.hist, color='magenta')
            self.triangle, = ax.plot(stats.median, stats.median_val, marker='v', color='crimson')
            self.dot, = ax.plot(stats.mean, stats.mean_val, marker='o', color='crimson')
            self.dotted_vline_left = ax.axvline(stats.stdev_left, color='magenta', linestyle=':')
            self.dotted_vline_right = ax.axvline(stats.stdev_right, color='magenta', linestyle=':')

