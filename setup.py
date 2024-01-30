#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-slow-first',
    version='1.0.3',
    author='João Vitor Silvestre',
    author_email='joao_vitor_silvestre@outlook.com',
    maintainer='João Vitor Silvestre',
    maintainer_email='joao_vitor_silvestre@outlook.com',
    license='MIT',
    url='https://github.com/joaovitorsilvestre/pytest-slow-first',
    description='Prioritize running the slowest tests first.',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    py_modules=['pytest_slow_first'],
    python_requires='>=3.5',
    install_requires=['pytest>=3.5.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'slow-first = pytest_slow_first',
        ],
    },
)
