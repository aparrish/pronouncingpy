.. pronouncing documentation master file, created by
   sphinx-quickstart on Tue Jul  9 22:26:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Documentation for pronouncing
=============================

Pronouncing is a simple interface for the `CMU Pronouncing Dictionary
<http://www.speech.cs.cmu.edu/cgi-bin/cmudict>`_. The library is designed to be
easy to use, and has no external dependencies. For example, here's all you need
to do in order to find rhymes for a given word::

    >>> import pronouncing
    >>> pronouncing.rhymes("climbing")
    ['diming', 'liming', 'priming', 'rhyming', 'timing']

Read the documentation here: https://pronouncing.readthedocs.org.

I made this library because I wanted to be able to use the CMU Pronouncing
Dictionary in my projects without having to install the grand behemoth that is
NLTK. It's designed to be friendly to beginner programmers who want to get
started with creative language generation and analysis, and for experts who
want to make quick prototypes of projects that deal with English pronunciation.

Installation
------------

Install with pip like so::

    pip install pronouncing

You can also download the source code and install manually::

    python setup.py install

Contents
--------

.. toctree::
   :maxdepth: 2

   tutorial
   pronouncing
   authors
   history

