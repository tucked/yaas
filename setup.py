# coding: utf-8

import setuptools
import subprocess

from yaas import __version__

setuptools.setup(
    name='yaas',
    version=__version__,
    license='MIT',
    description="Yet Another Ambari Shell",
    url="https://github.com/dmtucker/yaas",
    packages=['yaas'],
    entry_points={ 'console_scripts': [ "yaas = yaas.cmd:main" ] }
    )

