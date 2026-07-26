from ColorCard import ColorCard
from OklchPlotter import OklchPlotter
import Reader
import Writer


def example():
    card = ColorCard(img_format='png')
    thread_pic = card.create_thread_pic('666')
    lookup_file = 'lord_libidan_hexcodes.csv'
    lookup = Reader.create_oklch_dict_from_hexcodes(lookup_file)
    reference = lookup[thread_pic.thread_id]
    csv_lines = [Writer.get_stats_csv_header()]
    plotter = OklchPlotter(thread_pic, reference)
    csv_lines.append(Writer.get_stats_csv_line(plotter))
    Writer.save_stats_csv(csv_lines, 'stats_666.csv')
    plotter.plot_combo_lch()
    plotter.save('')
    plotter.show()


if __name__ == '__main__':
    example()


