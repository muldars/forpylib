#!/usr/bin/env python

from setuptools import setup, find_packages
from os import path
import sys
import os

# add the pyudev source directory to our path
doc_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.normpath(
    os.path.join(doc_directory, os.pardir)))


class Mock(object):
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return Mock()

    @classmethod
    def __getattr__(cls, name):
        if name in ('__file__', '__path__'):
            return '/dev/null'
        elif name[0] == name[0].upper():
            mockType = type(name, (), {})
            mockType.__module__ = __name__
            return mockType
        else:
            return Mock()

MOCK_MODULES = ['numpy', 'matplotlib', 'matplotlib.pyplot', 'pandas']
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = Mock()



LICENSE = open('LICENSE').read()


v = open(path.join(path.dirname(__file__), 'VERSION'))
VERSION = v.readline().strip()
v.close()



LONG_DESCRIPTION = open('README.md').read().replace("`_", "`")
setup(
    name='forpylib',
    version=VERSION,
    description='A Python library for forest optimization & simulation',
    long_description=open('README.md').read(),
    author='UXFS Statistics & Operations Research Team (UXFSort)',
    author_email='josemario.gonzalez@usc.es',
    url='http://bitbucket.org/forostm/forpylib.git',
    packages=['forpylib'],
    license='GPLv3',
    keywords=[
        'forest', 'simulator', 'DSS','optimization'
        'decision', 'support', 'system','growth'
    ],
    install_requires=['numpy', 'pandas', 'matplotlib'],
    zip_safe=False,
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Forest Management'
        ))
