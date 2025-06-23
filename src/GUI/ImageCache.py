from pathlib import Path
import os
import urllib.request

class ImageCache:
    cache_path = Path('./cached_images')

    @classmethod
    def fetch_image(cls, checksum, link):
        if not os.path.exists(cls.cache_path):
            os.makedirs(cls.cache_path)

        for file in os.listdir(cls.cache_path):
            if str(checksum) == file[:file.index('.')]:
                with open(cls.cache_path / Path(file), mode='rb') as opened_file:
                    return opened_file.read()

        try:
            print(f'Fetching profile pic from {link}...')
            request = urllib.request.urlretrieve(link, cls.cache_path / Path(f'{checksum}.jpg'))
        except ValueError:
            with open(Path(link), mode='rb') as file:
                return file.read()

        with open(cls.cache_path / Path(f'{checksum}.jpg'), mode='rb') as file:
            return file.read()

