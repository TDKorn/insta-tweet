.. _getting-started:

Getting Started
---------------------

InstaTweet Profiles
~~~~~~~~~~~~~~~~~~~~~~~~~~~
**InstaTweet** uses the :class:`~.Profile` class to help manage Twitter accounts, Instagram sessions, and user maps.

.. autoclass:: InstaTweet.profile.Profile
   :no-members:
   :noindex:


.. _settings:

Profile Settings
~~~~~~~~~~~~~~~~~~~

All settings can be configured in two ways:

1. By passing them as keyword arguments when initializing a :class:`~.Profile`
2. By setting them directly as object attributes after the :class:`~.Profile` object is created


.. _mandatory-settings:

Mandatory Settings
===================

* ``session_id`` — Instagram Sessionid Cookie, obtained by logging in on a desktop browser
* ``twitter_keys`` — Twitter API Keys with v1.1 endpoint access

Mandatory Settings with Default Values
=========================================

* ``name="default"`` — profile name; if non-default, it must be unique
* ``local=True`` — Indicates if the profile should be saved locally (default) or on a remote database
* ``user_agent=USER_AGENT`` — User agent to use when making requests to Instagram


Entirely Optional Settings
=========================================

* ``proxy_key`` — Environment variable to retrieve proxies from when making requests to Instagram/Twitter
* ``user_map`` — Fully formatted dictionary of IG usernames mapped to their ``USER_MAPPING``


Creating a Profile
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from InstaTweet import Profile

    # Initialize a profile with arguments
    p = Profile(
        name='myProfile',
        session_id='6011991A'
    )

    # Initialize a profile with no arguments
    q = Profile()
    q.name = 'myProfile'
    q.session_id = '6011991A'


All settings can be accessed via the :attr:`~.Profile.config` dict.
If you just want to look, call :meth:`~.view_config`

.. code-block:: python

    # View and compare configuration settings
    >>> q.view_config()
    >>> print(f'Same Config: {p.config==q.config}')


Output:

.. code-block:: shell

    name : myProfile
    local : True
    session_id : 6011991A
    twitter_keys : {'Consumer Key': 'string', 'Consumer Secret': 'string', 'Access Token': 'string', 'Token Secret': 'string'}
    user_agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36
    proxy_key : None
    user_map : {}
    Same Config: True


...

.. admonition:: Validating Profile Settings
   :class: instatweet:

   * Property setters validate data types for the :ref:`mandatory-settings`
   * Requirements aren't strictly enforced until :meth:`~.InstaTweet.start` is called,
     which will first :meth:`~.Profile.validate` the profile settings


Populating the User Map
~~~~~~~~~~~~~~~~~~~~~~~~~~

The User Map
==============

The :attr:`~.user_map` allows a :class:`~.Profile` to maintain
a history of package-related activity for its added IG users


Users are mapped to their :attr:`~.USER_MAPPING`, which contains their associated lists of:

.. code-block:: python

    USER_MAPPING = {'hashtags': [], 'scraped': [], 'tweets': []}


* ``hashtags`` — the user's associated hashtag list (for use when composing tweets)
* ``scraped`` — the list of posts that have been scraped from the user (only the post id)
* ``tweets`` — the list of sent tweets containing media scraped from that user (limited data)


The mapping gets updated each time :class:`~.InstaTweet` successfully scrapes and tweets a post from the user



Adding Users
=================

Use the :meth:`~.add_users` method to add one or more Instagram users
to a :class:`~.Profile`'s :attr:`~.user_map`

.. code-block:: python

    from InstaTweet import Profile

    # Add one user at a time
    >>> p = Profile('myProfile')
    >>> p.add_users('the.dailykitten', send_tweet=True)

    Added Instagram user @the.dailykitten to the user map

    # Add multiple users at once
    >>> usernames = ['dailykittenig','the.daily.kitten.ig']
    >>> p.add_users(usernames)

    Added Instagram user @dailykittenig to the user map
    Added Instagram user @the.daily.kitten.ig to the user map


The :meth:`~.Profile.get_user` method can be used to retrieve the full :attr:`~.USER_MAPPING` of an added user

.. code-block:: python

    >> p.get_user('the.dailykitten')

    {'hashtags': [], 'scraped': [-1], 'tweets': []}


Adding Hashtags
=================

You can :meth:`~.add_hashtags` for each user in the :attr:`~.user_map`

* They'll be chosen from at random when composing tweets based on one of their :attr:`~.posts`
* For more info, see :meth:`~.pick_hashtags`, :meth:`~.build_tweet` and :meth:`~.send_tweet`

.. code-block:: python

    # Add a single hashtag for a specific user
    >>> p.add_hashtags(user='dailykittenig', hashtags='cats')

    Added hashtags for @dailykittenig

    # Add multiple hashtags at once
    >>> users = ['the.dailykitten','the.daily.kitten.ig']
    >>> hashtags = ['kittygram', 'kittycat']

    >>> for user in users:
    ...     p.add_hashtags(user, hashtags)

    Added hashtags for @the.dailykitten
    Added hashtags for @the.daily.kitten.ig

    >>> p.view_config()


Output:

.. code-block:: shell

    name : myProfile
    local : True
    session_id : 6011991A
    twitter_keys : {'Consumer Key': 'string', 'Consumer Secret': 'string', 'Access Token': 'string', 'Token Secret': 'string'}
    user_agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36
    proxy_key : None
    user_map : {'the.dailykitten': {'hashtags': ['kittygram', 'kittycat'], 'scraped': [-1], 'tweets': []}, 'dailykittenig': {'hashtags': ['cats'], 'scraped': [], 'tweets': []}, 'the.daily.kitten.ig': {'hashtags': ['kittygram', 'kittycat'], 'scraped': [], 'tweets': []}}



User Map Access Methods
===========================

.. admonition:: User Map Access Methods
    :class: instatweet

    The :class:`~.Profile` has several methods that allow for easy access to the :attr:`~.user_map`

    * :meth:`~.Profile.get_user` provides access to a particular user's :attr:`~.USER_MAPPING`
    * :meth:`~.get_scraped_from` returns the list of posts scraped from a specified user
    * :meth:`~.get_hashtags_for` returns the list of hashtags to use in tweets for the specified user
    * :meth:`~.get_tweets_for` returns a list of tweets that use the specified user's scraped content


All lists returned by these methods can be modified in place. For example:

.. code-block:: python

    # View the list of hashtags by username
    >> print(p.get_hashtags_for('the.daily.kitten.ig'))

    ['kittygram', 'kittycat']

    # Retrieve and modify the list
    >> p.get_hashtags_for('the.daily.kitten.ig').append('kittypoop')
    >> print(p.get_hashtags_for('the.daily.kitten.ig'))

    ['kittygram', 'kittycat', 'kittypoop']


Saving a Profile
~~~~~~~~~~~~~~~~~~~~~


.. include:: ../_snippets/save-profile.rst
    :start-line: 3


Although you don't *need* to :meth:`~.save` the Profile to :meth:`~.start` InstaTweet,
it's highly suggested since:

 * It's an easy way to group API settings together
 * It keeps track of previously scraped & tweeted posts, which is used to detect new posts


Example: Save a Profile
========================

.. note:: You can specify a new :attr:`~.Profile.name`
   for the profile in the call to :meth:`~.save`


.. code-block:: python

    from InstaTweet import Profile

    >>> p = Profile('myProfile')
    >>> p.save()

    Saved Local Profile myProfile

    >>> q = Profile()
    >>> q.save('aProfile')

    Saved Local Profile aProfile

    # Try to save under a name that's already used...
    >>> q.save('myProfile')

    FileExistsError: Local save file already exists for profile named "myProfile"
    Please choose another name, load the profile, or delete the file.

    >>> Profile.profile_exists("aProfile")
    True

