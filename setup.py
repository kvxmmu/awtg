from setuptools import setup, find_packages
from os.path import dirname, realpath, join

dir_ = dirname(realpath(__file__))
deps_file = join(dir_, 'requirements.txt')

with open(deps_file) as file:
    deps = file.read().splitlines()

setup(
    name='awtg',
    version='0.1',
    packages=find_packages(),
    install_requires=deps
)
