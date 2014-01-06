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
    """
    Mock modules.

    Taken from
    http://read-the-docs.readthedocs.org/en/latest/faq.html#i-get-import-errors-on-libraries-that-depend-on-c-modules
    with some slight changes.
    """

    @classmethod
    def mock_modules(cls, *modules):
        for module in modules:
            sys.modules[module] = cls()

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return self.__class__()

    def __getattr__(self, attribute):
        if attribute in ('__file__', '__path__'):
            return os.devnull
        else:
            # return the *class* object here.  Mocked attributes may be used as
            # base class in pyudev code, thus the returned mock object must
            # behave as class, or else Sphinx autodoc will fail to recognize
            # the mocked base class as such, and "autoclass" will become
            # meaningless
            return self.__class__


# mock out native modules used throughout pyudev to enable Sphinx autodoc even
# if these modules are unavailable, as on readthedocs.org
Mock.mock_modules('numpy', 'matplotlib', 'matplotlib.pyplot', 'pandas')



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
