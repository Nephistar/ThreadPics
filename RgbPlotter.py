from matplotlib import pyplot as plt
import numpy as np

from ThreadPic import ThreadPic


class RgbPlotter:
    def __init__(self, thread: ThreadPic):
        self.thread = thread
        self.image_stat = self.thread.image_stat
        self.hist = self.thread.rgb_hist
        self._calc_rgb_stats()

    def _calc_rgb_stats(self):
        self.hist_red = self.hist[0: 255]
        self.hist_green = self.hist[256: 511]
        self.hist_blue = self.hist[512: 767]
        self.mean_red = round(self.image_stat.mean[0])
        self.mean_red_val = self.hist[self.mean_red]
        self.mean_green = round(self.image_stat.mean[1])
        self.mean_green_val = self.hist[256 + self.mean_green]
        self.mean_blue = round(self.image_stat.mean[2])
        self.mean_blue_val = self.hist[512 + self.mean_blue]
        self.median_rgb = self.image_stat.median
        self.median_red = self.median_rgb[0]
        self.median_red_val = self.hist[self.median_red]
        self.median_green = self.median_rgb[1]
        self.median_green_val = self.hist[256 + self.median_green]
        self.median_blue = self.median_rgb[2]
        self.median_blue_val = self.hist[512 + self.median_blue]
        self.mode_red_val = max(self.hist_red)
        self.mode_red = self.hist_red.index(self.mode_red_val)
        self.mode_green_val = max(self.hist_green)
        self.mode_green = self.hist_green.index(self.mode_green_val)
        self.mode_blue_val = max(self.hist_blue)
        self.mode_blue = self.hist_blue.index(self.mode_blue_val)

    def save(self, dir):
        path = dir + 'plot_' + self.thread.thread_id + '.png'
        plt.savefig(path)

    def show(self):
        plt.show()

    def plot_histogram_rgb(self):
        x = np.arange(255)
        fig, ax = plt.subplots()
        red_line, = ax.plot(x, self.hist_red, color='red')
        green_line, = ax.plot(x, self.hist_green, color='green')
        blue_line, = ax.plot(x, self.hist_blue, color='blue')
        red_dot, = ax.plot(self.mean_red, self.mean_red_val, marker='o', color='gold')
        green_dot, = ax.plot(self.mean_green, self.mean_green_val, marker='o', color='chartreuse')
        blue_dot, = ax.plot(self.mean_blue, self.mean_blue_val, marker='o', color='deepskyblue')
        red_triangle, = ax.plot(self.median_red, self.median_red_val, marker='v', color='gold')
        green_triangle, = ax.plot(self.median_green, self.median_green_val, marker='v', color='chartreuse')
        blue_triangle, = ax.plot(self.median_blue, self.median_blue_val, marker='v', color='deepskyblue')
        red_rectangle, = ax.plot(self.mode_red, self.mode_red_val, marker='s', color='gold')
        green_rectangle, = ax.plot(self.mode_green, self.mode_green_val, marker='s', color='chartreuse')
        blue_rectangle, = ax.plot(self.mode_blue, self.mode_blue_val, marker='s', color='deepskyblue')
        ax.legend((blue_rectangle, blue_triangle, blue_dot), ('mode', 'median', 'mean'))
        ax.set_xlabel('value')
        ax.set_ylabel('pixel count')
        median_str = ' - median RGB: ' + str(self.median_rgb)
        result = self.thread.thread_id + median_str
        ax.set_title(result)
        print(result)

