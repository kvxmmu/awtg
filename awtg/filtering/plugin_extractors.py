from importlib import import_module

from os.path import splitext
from os import listdir

PY_FILE_EXTS = {'.py'}


def has_extension(name, variants):
    return splitext(name)[1] in variants


def remove_extension(name):
    return splitext(name)[0]


def extract_from_dir(directory, importer=import_module):
    """
        Stupid plugins extractor
        use importer param to import plugin module from directory
    """

    files = listdir(directory)
    modules = []

    head_package = directory.replace('/', '.')

    for file in filter(lambda file_name: has_extension(file_name, PY_FILE_EXTS)
                       and not file_name.startswith('_'), files):
        package_name = head_package + '.' + remove_extension(file)

        modules.append(importer(package_name))

    return modules


