import sys
import os
from ofdtotext import OFDFile


def test():
    folder = 'ofds'
    for path in os.listdir(folder):
        if not path.endswith('.ofd'):
            continue
        print('read file', path)
        file_path = os.path.join(folder, path)
        doc = OFDFile(file_path)
        print(doc.get_text())


if __name__ == '__main__':
    file_path = sys.argv[1]
    doc = OFDFile(file_path)
    print(doc.get_text())
