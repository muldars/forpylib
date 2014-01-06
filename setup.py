#!/usr/bin/env python

from setuptools import setup, find_packages
from os import path




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
