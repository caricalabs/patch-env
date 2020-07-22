#!/usr/bin/env python3
"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='patch_env',
    version='1.0.0',
    description='Patch os.environ with dynamic values when the interpreter starts',
    long_description=long_description,
    url='https://github.com/caricalabs/patch-env',
    author='Carica Labs, LLC',
    author_email='info@caricalabs.com',
    license='APL 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='patch environment dynamic hook os.environ',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[],
    extras_require={'dev': ['check-manifest'], 'test': []},
    package_data={},
    data_files=[('/', ["patch_env.pth"])],
)
