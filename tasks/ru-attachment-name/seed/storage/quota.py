import os


def folder_size(folder):
    return sum(os.path.getsize(os.path.join(folder, f)) for f in os.listdir(folder))
