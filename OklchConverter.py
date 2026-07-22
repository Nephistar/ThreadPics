import statistics

import oklch


class Datum:
    def __init__(self, rgb: tuple[int, int, int]):
        self.rgb = rgb
        self.oklch = oklch.srgb_to_oklch(rgb)
        self.ok_lightness = self.oklch[0]
        self.ok_chroma = self.oklch[1]
        self.ok_hue = self.oklch[2]
        # arbitrary decision to round and measure the values in the following way
        # Lightness in three per mille steps
        self.lightness_for_hist = int(round(self.ok_lightness / 3 * 1000))
        # Chroma in one per mille steps
        self.chroma_for_hist = int(round(self.ok_chroma * 1000))
        # Hue in one degree steps
        self.hue_for_hist = int(round(self.ok_hue))


class Histogram:
    def __init__ (self, rgbs):
        self.rgbs = rgbs
        self.data = []
        for rgb in self.rgbs:
            datum = Datum(rgb)
            self.data.append(datum)
        self.data_lightness = []
        self.data_chroma = []
        self.data_hue = []
        # define histogram limits according to the decided step sizes
        self.lower_limit_lightness = 0
        self.upper_limit_lightness = 333
        self.hist_lightness = [0] * (self.upper_limit_lightness + 1)
        self.lower_limit_chroma = 0
        self.upper_limit_chroma = 370
        self.hist_chroma = [0] * (self.upper_limit_chroma + 1)
        self.lower_limit_hue = 0
        self.upper_limit_hue = 359
        self.hist_hue = [0] * (self.upper_limit_hue + 1)
        for datum in self.data:
            self.data_lightness.append(datum.lightness_for_hist)
            self.data_chroma.append(datum.chroma_for_hist)
            self.data_hue.append(datum.hue_for_hist)
        self._check_limits()
        self._fill_histogram(self.hist_lightness, self.data_lightness)
        self._fill_histogram(self.hist_chroma, self.data_chroma)
        self._fill_histogram(self.hist_hue, self.data_hue)
        # Lightness
        self.mode_lightness = statistics.mode(self.data_lightness)
        self.median_lightness = int(round(statistics.median(self.data_lightness)))
        self.mean_lightness = int(round(statistics.mean(self.data_lightness)))
        self.standard_deviation_lightness = statistics.pstdev(self.data_lightness, self.mean_lightness)
        self.stdev_left_lightness = self.mean_lightness - self.standard_deviation_lightness
        self.stdev_right_lightness = self.mean_lightness + self.standard_deviation_lightness
        self.mode_lightness_val = self.hist_lightness[self.mode_lightness]
        self.median_lightness_val = self.hist_lightness[self.median_lightness]
        self.mean_lightness_val = self.hist_lightness[self.mean_lightness]
        # Chroma
        self.mode_chroma = statistics.mode(self.data_chroma)
        self.median_chroma = int(round(statistics.median(self.data_chroma)))
        self.mean_chroma = int(round(statistics.mean(self.data_chroma)))
        self.standard_deviation_chroma = statistics.pstdev(self.data_chroma, self.mean_chroma)
        self.stdev_left_chroma = self.mean_chroma - self.standard_deviation_chroma
        self.stdev_right_chroma = self.mean_chroma + self.standard_deviation_chroma
        self.mode_chroma_val = self.hist_chroma[self.mode_chroma]
        self.median_chroma_val = self.hist_chroma[self.median_chroma]
        self.mean_chroma_val = self.hist_chroma[self.mean_chroma]
        # Hue is circular (or periodical), so median and mean don't work without a trick.
        # In this special usecase, all values will be within a small interval.
        # Therefore, we can just work with an offset of 180 to avoid clipping over the edge.
        self.mode_hue = statistics.mode(self.data_hue)
        if self.mode_hue < 180 or self.mode_hue >= 270:
            data_hue_off = []
            for hue in self.data_hue:
                hue_off = (hue + 180) % 360
                data_hue_off.append(hue_off)
            median_hue_off = int(round(statistics.median(data_hue_off)))
            mean_hue_off = int(round(statistics.mean(data_hue_off)))
            standard_deviation_hue_off = statistics.pstdev(data_hue_off, mean_hue_off)
            stdev_left_hue_off = mean_hue_off - standard_deviation_hue_off
            stdev_right_hue_off = mean_hue_off + standard_deviation_hue_off
            self.median_hue = (median_hue_off + 180) % 360
            self.mean_hue = (mean_hue_off + 180) % 360
            self.standard_deviation_hue = (standard_deviation_hue_off + 180) % 360
            self.stdev_left_hue = (stdev_left_hue_off + 180) % 360
            self.stdev_right_hue = (stdev_right_hue_off + 180) % 360
        else:
            self.median_hue = int(round(statistics.median(self.data_hue)))
            self.mean_hue = int(round(statistics.mean(self.data_hue)))
            self.standard_deviation_hue = statistics.pstdev(self.data_hue, self.mean_hue)
            self.stdev_left_hue = self.mean_hue - self.standard_deviation_hue
            self.stdev_right_hue = self.mean_hue + self.standard_deviation_hue
        self.mode_hue_val = self.hist_hue[self.mode_hue]
        self.median_hue_val = self.hist_hue[self.median_hue]
        self.mean_hue_val = self.hist_hue[self.mean_hue]

    # weird little data check: quick, dirty, and insufficient
    def _check_limits (self):
        error = ''
        message = 'ERROR with Oklch data calculation: '
        extremum = min(self.data_lightness)
        if extremum < self.lower_limit_lightness:
            error += message + 'lightness under ' + str(self.lower_limit_lightness) + ': ' + str(extremum) + '\n'
        extremum = max(self.data_lightness)
        if extremum > self.upper_limit_lightness:
            error += message + 'lightness over ' + str(self.upper_limit_lightness) + ': ' + str(extremum) + '\n'
        extremum = min(self.data_chroma)
        if extremum < self.lower_limit_chroma:
            error += message + 'chroma under ' + str(self.lower_limit_chroma) + ': ' + str(extremum) + '\n'
        extremum = max(self.data_chroma)
        if extremum > self.upper_limit_chroma:
            error += message + 'chroma over ' + str(self.upper_limit_chroma) + ': ' + str(extremum) + '\n'
        extremum = min(self.data_hue)
        if extremum < self.lower_limit_hue:
            error += message + 'hue under ' + str(self.lower_limit_hue) + ': ' + str(extremum) + '\n'
        extremum = max(self.data_hue)
        if extremum > self.upper_limit_hue:
            error += message + 'hue over ' + str(self.upper_limit_hue) + ': ' + str(extremum) + '\n'
        if error != '':
            print(error)

    def _fill_histogram(self, hist: list[int], data: list[int]):
        for val in data:
            if val < len(hist):
                hist[val] += 1
        return hist

