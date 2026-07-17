from PIL import Image
from PIL.ImageStat import Stat

from OklchConverter import Histogram


class ThreadPic:
    def __init__(self, thread_id: str, image_path: str):
        self.thread_id = thread_id
        self.image_path = image_path
        self.image = Image.open(self.image_path)
        with Image.open(self.image_path) as im:
            pixel_access = im.load()
        self.pixels = []
        for x in range(0, self.image.size[0]):
            for y in range(0, self.image.size[1]):
                self.pixels.append(pixel_access[x, y])
        self.image_stat = Stat(self.image)
        self.rgb_hist = self.image.histogram()
        self.oklch = Histogram(self.pixels)

