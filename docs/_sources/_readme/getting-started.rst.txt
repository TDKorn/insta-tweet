.. _getting-started:

Getting Started
---------------------

InstaTweet Profiles
~~~~~~~~~~~~~~~~~~~~~~~~~~~
**InstaTweet** uses the :class:`~.Profile` class to help manage Twitter accounts, Instagram sessions, and page maps.

.. autoclass:: InstaTweet.profile.Profile
   :no-members:
   :noindex:


.. _settings:

Profile Settings
~~~~~~~~~~~~~~~~~~~


.. _mandatory-settings:

Mandatory Settings
===================

* :attr:`~.session_id` — Instagram sessionid cookie, obtained by logging in on a desktop browser
* :attr:`~.twitter_keys` — Twitter API keys with v1.1 endpoint access

Mandatory Settings with Default Values
=========================================

* :attr:`~.Profile.name` (``="default"``) — the profile name; if non-default, it must be unique
* :attr:`~.Profile.local` (``=True``) — indicates if the profile should be saved locally (default) or on a remote database
* ``user_agent=USER_AGENT`` — user agent to use when making requests to Instagram; currently hardcoded


Entirely Optional Settings
=========================================

* ``proxy_key`` — Environment variable to retrieve proxies from when making requests to Instagram/Twitter
* :attr:`~.page_map` — Fully formatted dictionary of IG pages mapped to their ``PAGE_MAPPING``


Creating a Profile
~~~~~~~~~~~~~~~~~~~~~~~

Profile settings can be configured

1. By passing them as keyword arguments when initializing a :class:`~.Profile`
2. By setting them directly as object attributes after the :class:`~.Profile` object is created


.. code-block:: python

    from InstaTweet import Profile

    # Initialize a profile with arguments
    p = Profile('myProfile', session_id='6011991A')

    # Initialize a profile with no arguments
    q = Profile()
    q.name = 'myProfile'
    q.session_id = '6011991A'


All settings can be accessed via the :attr:`~.Profile.config` dict,
which can be pretty printed using :meth:`~.view_config`

.. code-block:: python

    # View and compare configuration settings
    >>> q.view_config()


.. code-block:: shell

    name : myProfile
    local : True
    session_id : 6011991A
    twitter_keys : {'Consumer Key': 'string', 'Consumer Secret': 'string', 'Access Token': 'string', 'Token Secret': 'string'}
    user_agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36
    proxy_key : None
    page_map : {}

...

.. admonition:: Validating Profile Settings
   :class: instatweet:

   * Property setters validate data types for the :ref:`mandatory-settings`
   * Requirements aren't strictly enforced until :meth:`~.InstaTweet.start` is called,
     which will first :meth:`~.Profile.validate` the profile settings


Populating the Page Map
~~~~~~~~~~~~~~~~~~~~~~~~~~

The Page Map
==============

The :attr:`~.page_map` allows a :class:`~.Profile` to maintain
a history of package-related activity for its added IG pages (users or hashtags).


Pages are mapped to their :attr:`~.PAGE_MAPPING`, which contains their associated lists of:

.. code-block:: python

    PAGE_MAPPING = {'hashtags': [], 'scraped': [], 'tweets': []}


* ``hashtags`` — the page's associated hashtag list (for use when composing tweets)
* ``scraped`` — the list of posts that have been scraped from the page (only the post id)
* ``tweets`` — the list of sent tweets containing media scraped from that page (limited data)


The mapping gets updated each time :class:`~.InstaTweet` successfully scrapes and tweets a post from the page



Adding Pages
=================

Use the :meth:`~.add_pages` method to add one or more Instagram pages
to a :class:`~.Profile`'s :attr:`~.page_map`

.. code-block:: python

    from InstaTweet import Profile

    # Add one page at a time
    >>> p = Profile('myProfile')
    >>> p.add_pages('the.dailykitten', send_tweet=True)

    Added Instagram page @the.dailykitten to the page map

    # Add multiple pages at once
    >>> pages = ['dailykittenig','#thedailykitten']
    >>> p.add_pages(pages)

    Added Instagram page @dailykittenig to the page map
    Added Instagram page #thedailykitten to the page map


The :meth:`~.Profile.get_page` method can be used to retrieve the full :attr:`~.PAGE_MAPPING` of an added page

.. code-block:: python

    >> p.get_page('the.dailykitten')

    {'hashtags': [], 'scraped': [-1], 'tweets': []}


Adding Hashtags
=================

You can :meth:`~.add_hashtags` for each page in the :attr:`~.page_map`

* They'll be chosen from at random when composing tweets based on one of their :attr:`~.posts`
* For more info, see :meth:`~.pick_hashtags`, :meth:`~.build_tweet` and :meth:`~.send_tweet`

.. code-block:: python

    # Add a single hashtag for a specific page
    >>> p.add_hashtags('dailykittenig', 'cats')

    Added hashtags for dailykittenig

    # Add multiple hashtags at once
    >>> pages = ['the.dailykitten', '#thedailykitten']
    >>> hashtags = ['kittygram', 'kittycat']

    >>> for page in pages:
    ...     p.add_hashtags(page, hashtags)

    Added hashtags for the.dailykitten
    Added hashtags for #thedailykitten

    >>> p.view_config()


.. code-block:: shell

    name : myProfile
    local : True
    session_id : 6011991A
    twitter_keys : {'Consumer Key': 'string', 'Consumer Secret': 'string', 'Access Token': 'string', 'Token Secret': 'string'}
    user_agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36
    proxy_key : None
    page_map : {'the.dailykitten': {'hashtags': ['kittygram', 'kittycat'], 'scraped': [-1], 'tweets': []}, 'dailykittenig': {'hashtags': ['cats'], 'scraped': [], 'tweets': []}, '#thedailykitten': {'hashtags': ['kittygram', 'kittycat'], 'scraped': [], 'tweets': []}}



Page Map Access Methods
===========================

.. admonition:: Page Map Access Methods
    :class: instatweet

    The :class:`~.Profile` has several methods that allow for easy access to the :attr:`~.page_map`

    * :meth:`~.Profile.get_page` provides access to a particular page's :attr:`~.PAGE_MAPPING`
    * :meth:`~.get_scraped_from` returns the list of posts scraped from a specified page
    * :meth:`~.get_hashtags_for` returns the list of hashtags to use in tweets for the specified page
    * :meth:`~.get_tweets_for` returns a list of tweets that use the specified page's scraped content



.. include:: ../_snippets/save-profile.rst


.. include:: /_snippets/run-profile.rst
