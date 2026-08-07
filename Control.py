from ColorCard import ColorCard
from OklchPlotter import OklchPlotter
import Reader
import Writer

class Control:
    def __init__(self, args: dict):
        self.plot_mode = bool(args['--plot'])
        self.show_mode = bool(args['--show'])
        self.example_mode = bool(args['--example'])
        self.ref_file = args['<ref_file>']
        self.img_dir = args['<img_dir>']
        self.stats_file = args['<stats_file>']
        self.plot_dir = args['<plot_dir>']
        self.lookup = None
        self.card = None
        self.run()

    def run(self):
        if self.example_mode:
            self.plot_mode = True
            self.show_mode = True
        self.process_dir()

    def process_dir(self):
        self.lookup = Reader.create_oklch_dict_from_hexcodes(self.ref_file)
        self.card = ColorCard(self.img_dir)
        csv_lines = [Writer.get_stats_csv_header()]
        first_flag = True
        for thread_pic in self.card.thread_pics:
            reference = self.lookup[thread_pic.thread_id]
            plotter = OklchPlotter(thread_pic, reference)
            show_flag = first_flag and self.show_mode
            if self.plot_mode:
                self.plot(plotter, show_flag)
            first_flag = False
            csv_lines.append(Writer.get_stats_csv_line(plotter))
        Writer.save_stats_csv(csv_lines, self.stats_file)

    def plot(self, plotter: OklchPlotter, show_flag: bool):
        plotter.plot_combo_lch()
        plotter.save(self.plot_dir)
        if show_flag:
            plotter.show()
        else:
            plotter.close()

