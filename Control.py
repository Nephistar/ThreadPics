from ColorCard import ColorCard
from OklchPlotter import OklchPlotter
import PicFetcher
import Reader
import Writer

class Control:
    def __init__(self, args: dict):
        self.fetch_mode = bool(args['--fetch'])
        self.plot_mode = bool(args['--plot'])
        self.show_mode = bool(args['--show'])
        self.hue_flag = bool(args['--hue'])
        self.lc_flag = bool(args['--lc'])
        self.set_window = bool(args['--set_window'])
        self.example_mode = bool(args['--example'])
        self.url_file = args['<url_file>']
        self.save_dir = args['<save_dir>']
        self.lch_y_top = args['<lch_y_top>']
        self.ref_file = args['<ref_file>']
        self.img_dir = args['<img_dir>']
        self.stats_file = args['<stats_file>']
        self.plot_dir = args['<plot_dir>']
        self.lookup = None
        self.card = None
        self.run()

    def run(self):
        if self.fetch_mode:
           PicFetcher.fetch(self.url_file, self.save_dir)
        else:
            if self.example_mode:
                self.plot_mode = True
                self.show_mode = True
            self.process_dir()

    def process_dir(self):
        self.lookup = Reader.create_oklch_dict_from_hexcodes(self.ref_file)
        self.card = ColorCard(self.img_dir)
        if self.set_window:
            self.lch_y_top = int(self.lch_y_top)
        else:
            self.lch_y_top = int(self.card.pixel_max / 10)
        csv_lines = [Writer.get_stats_csv_header()]
        first_flag = True
        for thread_pic in self.card.thread_pics:
            reference = self.lookup[thread_pic.thread_id]
            plotter = OklchPlotter(thread_pic, reference)
            show_flag = first_flag and self.show_mode
            if self.plot_mode:
                self.plot(plotter, show_flag, self.lch_y_top)
            first_flag = False
            csv_lines.append(Writer.get_stats_csv_line(plotter))
        Writer.save_stats_csv(csv_lines, self.stats_file)

    def plot(self, plotter: OklchPlotter, show_flag: bool, lch_y_top: int):
        # Note: Hue plot has to come before the combined ones. This is a quickfix for a potential bug
        # with aranging the width. It works fine when done in order from narrowest to widest.
        if self.hue_flag:
            plotter.plot_hue()
            plotter.save(self.plot_dir)
        if self.lc_flag:
            plotter.plot_combo_lc()
            plotter.save(self.plot_dir)
        plotter.plot_combo_lch(lch_y_top)
        plotter.save(self.plot_dir)
        if show_flag:
            plotter.show()
        else:
            plotter.close()
            plotter.close()
            plotter.close()

