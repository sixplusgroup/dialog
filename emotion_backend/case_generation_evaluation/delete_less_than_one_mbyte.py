import os


def delete_less_than_size(dir_path, size):
    for root, dirs, filenames in os.walk(dir_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if os.path.getsize(file_path) <= size:
                os.remove(file_path)


if __name__ == '__main__':
    delete_less_than_size('TODO/wav_new', 1024 * 1024)
