#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pronouncing',
    version='0.1.5',
    description="A simple interface for the CMU pronouncing dictionary",
    long_description=readme + '\n\n' + history,
    author="Allison Parrish",
    author_email='allison@decontextualize.com',
    url='https://github.com/aparrish/pronouncingpy',
    packages=[
        'pronouncing',
    ],
    package_dir={'pronouncing':
                 'pronouncing'},
    package_data={'pronouncing': ['cmudict-0.7b']},
    install_requires=requirements,
    license="BSD",
    zip_safe=True,
    keywords='pronouncing',
    classifiers=[
        "Development Status :: 3 - Alpha",
        'License :: OSI Approved :: BSD License',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Artistic Software",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    test_suite='tests',
    tests_require=test_requirements
)
