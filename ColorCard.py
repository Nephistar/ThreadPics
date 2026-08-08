import os

from ThreadPic import ThreadPic


class ColorCard:
    def __init__(self, dir: str, size_limit: int=50000):
        self.dir_path = dir
        self.size_limit = size_limit
        self.thread_pics = []
        self.pixel_max = 0
        self._create_all_thread_pics()

    def _create_thread_pic(self, thread_id: str, img_path: str) -> ThreadPic:
        thread_pic = ThreadPic(thread_id, img_path)
        return thread_pic

    def _create_all_thread_pics(self):
        for file in os.listdir(self.dir_path):
            path = os.path.join(self.dir_path, file)
            if os.path.isfile(path):
                thread_id = file[:file.rfind('.')]
                if os.path.getsize(path) > self.size_limit:
                    print('The following file is over the size limit of '
                          + str(self.size_limit) + ' B and got skipped: ' + path)
                else:
                    thread_pic = self._create_thread_pic(thread_id, path)
                    self.thread_pics.append(thread_pic)
                    if len(thread_pic.pixels) > self.pixel_max:
                        self.pixel_max = len(thread_pic.pixels)
        return self.thread_pics

