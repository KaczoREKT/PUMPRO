import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def read_file(file_path):
    path = resource_path(file_path)
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()