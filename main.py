from ColorCard import ColorCard
from OklchPlotter import OklchPlotter


def example():
    card = ColorCard(img_format='png')
    thread_pic = card.create_thread_pic('666')
    plotter = OklchPlotter(thread_pic)
    plotter.plot_combo_lch()
    plotter.save('')
    plotter.show()


if __name__ == '__main__':
    example()


