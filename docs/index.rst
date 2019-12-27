kenpompy: College Basketball for Nerds
======================================
.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. image:: https://github.com/j-andrews7/kenpompy/raw/master/docs/_static/images/kenpompy_unsplash.png 
	:alt: kenpompy logo

This python package serves as a convenient web scraper for `kenpom <kenpom.com>`_, which provides tons of great NCAA basketball statistics and metrics. It **requires a subscription to KenPomeroy's site for use**, otherwise only the home page will be accessible. It's a small fee for a year of access, and totally worth it in my opinion.

Objective
=========

Ultimately, this package is to allow both hobbyist and reknown sports analysts alike to get data from kenpom in a format more suitable for visualization, transformation, and additional analysis. It's meant to be simple, easy to use, and to yield information in a way that is immediately usable.

Responsible Use
===============

As with many web scrapers, the responsibility to use this package in a reasonable manner falls upon the user. Don't be a jerk and constantly scrape the site a thousand times a minute or you run the risk of potentially getting barred from it, which you'd likely deserve. I am in no way responsible for how you use (or abuse) this package. Be sensible.

But I Use R
===========

Yeah, yeah, but have you heard of `reticulate <https://rstudio.github.io/reticulate/>`_? It's an R interface to python that also supports passing objects (like dataframes!) between them. 

Installation
============

:code:`kenpompy` is easily installed via :code:`pip`::

	pip install kenpompy


What It Can (and Can't) Do
==========================

This a work in progress - it can currently scrape all of the summary and miscellaneous tables, pretty much all of those under the Stats and Miscellany headings. :code:`Team` and :code:`Player` classes are planned, but they're more complicated and will take some time.

Usage
=====

:code:`kenpompy` is simple to use. Generally, tables on each page are scraped into :code:`pandas` dataframes with simple parameters to select different seasons or tables. As many tables have headers that don't parse well, some are manually altered to a small degree to make the resulting dataframe easier to interpret and manipulate. 

First, you must login::

	from kenpompy.utils import login

	# Returns an authenticated browser that can then be used to scrape pages that require authorization.
	browser = login(your_email, your_password)


Then you can request specific pages that will be parsed into convenient dataframes::

	import kenpompy.summary as kp

	# Returns a pandas dataframe containing the efficiency and tempo stats for the current season (https://kenpom.com/summary.php).
	eff_stats = kp.get_efficiency(browser)


Full API Reference
==================

utils
-----

.. automodule:: kenpompy.utils
   :members:

misc
----

.. automodule:: kenpompy.misc
   :members:

summary
-------

.. automodule:: kenpompy.summary
   :members:

Contributing
============

You can contribute by creating `issues <https://github.com/j-andrews7/kenpompy/issues>`_ to highlight bugs and make suggestions for additional features. `Pull requests <https://github.com/j-andrews7/kenpompy/pulls>`_ are also welcome.

License
=======

`kenpompy` is released on the GNU GPL v3.0 license. You are free to use, modify, or redistribute it in almost any way, provided you state changes to the code, disclose the source, and use the same license. It is released with zero warranty for any purpose and I retain no liability for its use. `Read the full license <https://github.com/j-andrews7/kenpompy/blob/master/LICENSE>`_ for additional details.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
