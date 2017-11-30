#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of unit-utilization.
# https://github.com/garnertb/unit-utilization

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Tyler Garner <garnertb@prominentedge.com>

from setuptools import setup, find_packages

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]

setup(
    name='unit-utilization',
    version='0.0.1',
    description='Calculates the number of units out of service for a given time frame.',
    long_description='''
Calculates the number of units out of service for a given time frame.
''',
    keywords='utilization, fire service, public safety',
    author='Tyler Garner',
    author_email='garnertb@prominentedge.com',
    url='https://github.com/garnertb/unit-utilization',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        'click==6.7',
        'pandas==0.21.0',
        'numpy==1.13.3'
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
             'fiver=fiver:main',
        ],
    },
)
