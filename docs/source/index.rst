.. InstaTweet documentation master file, created by
   sphinx-quickstart on Sat Jul  9 06:46:42 2022.
.. index.rst
   Title comes from this file

.. include:: _readme/about-instatweet.rst
   :start-line: 2

.. TOC for sidebar (:hidden:)
   Using :glob: to have the bold caption as a "section title"
   It's basically like a page with a title and toctree except
   without the real title, you can avoid the extra level of nesting

.. toctree::
   :maxdepth: 2
   :caption: README
   :hidden:
   :glob:

   _readme/about-instatweet
   _readme/getting-started
   _readme/schedule_instatweet


InstaTweet README
~~~~~~~~~~~~~~~~~~~

.. Fake table of contents inserted after the "about-instatweet.rst" content
   Contains only title names, essentially like :maxdepth: 1 or :titlesonly:
   But without creating the TOC in the sidebar

* :ref:`about-insta-tweet`
* :ref:`getting-started`
* :ref:`schedule-insta-tweet`


.. The other toctrees are left as is (inserted + sidebar)

.. toctree::
   :maxdepth: 2
   :caption: Documentation
   :glob:

   modules


.. toctree::
   :maxdepth: 2
   :caption: Snippets
   :glob:

   snippets



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
