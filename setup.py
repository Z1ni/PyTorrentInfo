#!/usr/bin/env python3

from setuptools import setup

setup(name='PyTorrentInfo',
    version='0.1',
    description='Parse bencoded data (torrent files, tracker responses) using Python 3',
    author='Mark "zini" Mäkinen',
    author_email='marktmakinen@gmail.com',
    url='https://github.com/Z1ni/PyTorrentInfo',
    packages=['PyTorrentInfo'],
    package_dir={'': 'src'},
)
