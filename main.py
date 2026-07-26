from ColorCard import ColorCard
from OklchPlotter import OklchPlotter
import Reader


def example():
    card = ColorCard(img_format='png')
    thread_pic = card.create_thread_pic('666')
    lookup_file = 'lord_libidan_hexcodes.csv'
    lookup = Reader.create_oklch_dict_from_hexcodes(lookup_file)
    reference = lookup[thread_pic.thread_id]
    plotter = OklchPlotter(thread_pic, reference)
    plotter.plot_combo_lch()
    plotter.save('')
    plotter.show()


if __name__ == '__main__':
    example()


