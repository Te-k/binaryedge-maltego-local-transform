#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='binaryedge',
    author='Tek',
    version='1.0',
    author_email='tek@randhome.io',
    description='Maltego Transform for BinaryEdge https://www.binaryedge.io',
    license='GPLv3',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=False,
    package_data={
        '': ['*.gif', '*.png', '*.conf', '*.mtz', '*.machine']  # list of resources
    },
    install_requires=[
        'canari>=3.3.9,<4'
    ],
    dependency_links=[
        'pybinaryedge==0.2'
    ]
)
