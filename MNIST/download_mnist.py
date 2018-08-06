import requests
import gzip
from os import remove


def _download_files(urls, filenames):
    for i in range(len(urls)):
        print('Downloading: ' + urls[i])
        r = requests.get(urls[i])
        with open(filenames[i], 'wb') as file:
            for chunk in r.iter_content(chunk_size=1024):
                file.write(chunk)


def _unzip(filenames):
    for i in range(len(filenames)):
        print('Decompressing: ' + filenames[i])
        f = gzip.open(filenames[i], 'rb')
        file = open(filenames[i].split(sep='.gz', maxsplit=1)[0], 'wb')
        with gzip.open(filenames[i], 'rb') as gz:
            with open(filenames[i].split(sep='.gz')[0], 'wb') as file:
                while True:
                    data = gz.read(1024)
                    if not data:
                        break
                    file.write(data)
        remove(filenames[i])


_FILENAMES = ('train-images-idx3-ubyte.gz', 'train-labels-idx1-ubyte.gz',
             't10k-images-idx3-ubyte.gz', 't10k-labels-idx1-ubyte.gz')
_FILEURLS = ('http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz',
            'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz',
            'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz',
            'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz')


def get_mnist():
    _download_files(_FILEURLS, _FILENAMES)
    _unzip(_FILENAMES)