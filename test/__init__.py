from os import path, getcwd
from sys import path as sys_path

PROJECT_PATH = getcwd()
SOURCE_PATH = path.join(PROJECT_PATH, "src")

sys_path.append(SOURCE_PATH)
