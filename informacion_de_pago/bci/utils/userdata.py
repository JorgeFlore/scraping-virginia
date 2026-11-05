from os import makedirs, path, getcwd
from importlib import import_module
from time import time, sleep
from glob import glob
import shutil
import os
import sys

dir = path.join(getcwd(), "userdata")


def file(*p):
    return path.join(dir, *p)


def clean(extra_dirs: list[str] = []):
    shutil.rmtree(dir, True)

    for p in extra_dirs:
        makedirs(file(*p))


def all_files() -> list[str]:
    files = glob("**/*", root_dir="userdata", recursive=True)
    return [f for f in files if path.isfile(path.join("userdata", f))]

#banco = sys.argv[1]
""" def all_file():
    files = glob("**/*", root_dir="userdata/depositos/"+str(banco), recursive=True)
    return [f for f in files ] """
    


def wait_glob(p, timeout=100):
    end = time() + timeout

    while not glob(p, root_dir=dir):
        if time() > end:
            raise Exception("timeout")
        
        sleep(0.2)

    return glob(p, root_dir=dir)

def mv(a, b):
    shutil.move(file(a), file(b))
