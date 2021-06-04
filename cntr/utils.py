import os
import pathlib

def get_data_path(file):

    prefix = pathlib.Path(__file__).parent.resolve()
    return os.path.abspath(os.path.join(prefix, file))

if __name__ == '__main__':
    print(get_data_path('data/name.txt'))