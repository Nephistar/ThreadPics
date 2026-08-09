from scrapling.fetchers import Fetcher
from urllib.parse import urlparse
import Reader


def fetch(url_file: str, save_dir: str):
    lookup = Reader.create_url_dict(url_file)
    for thread_id in lookup:
        url = lookup[thread_id]
        parsed_url = urlparse(url)
        valid = parsed_url.scheme and parsed_url.netloc
        if valid:
            page = Fetcher.get(url)
            with open(file=save_dir + thread_id + '.jpg', mode='wb') as file:
                file.write(page.body)


if __name__ == '__main__':
    url_file = './tables/DMC_urls_482.csv'
    save_dir = './pics/'
    fetch(url_file, save_dir)

