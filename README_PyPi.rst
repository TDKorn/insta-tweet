.. meta::
   :title: InstaTweet - Automatically Repost Content From Instagram to Twitter
   :description: A Python package to automatically repost content from Instagram to Twitter

.. |.InstaTweet| replace:: ``InstaTweet``
.. _.InstaTweet: https://github.com/tdkorn/insta-tweet/blob/master/InstaTweet/instatweet.py#L5-L142
.. |.add_users| replace:: ``add_users()``
.. _.add_users: https://github.com/tdkorn/insta-tweet/blob/master/InstaTweet/profile.py#L167-L197
.. |.Profile| replace:: ``Profile``
.. _.Profile: https://github.com/tdkorn/insta-tweet/blob/master/InstaTweet/profile.py#L12-L416
.. |.start| replace:: ``start()``
.. _.start: https://github.com/tdkorn/insta-tweet/blob/master/InstaTweet/instatweet.py#L72-L117
.. |.InstaClient| replace:: ``InstaClient``
.. _.InstaClient: https://github.com/tdkorn/insta-tweet/blob/master/InstaTweet/instaclient.py#L14-L108
.. |mandatory-settings| replace:: mandatory settings
.. _mandatory-settings: https://instatweet.readthedocs.io/en/latest/_readme/getting-started.html#mandatory-settings

.. _about-insta-tweet:

✨🐥 InstaTweet 🐤✨
-----------------------

.. image:: https://img.shields.io/pypi/v/insta-tweet
   :target: https://pypi.org/project/insta-tweet/
   :alt: PyPI Version

.. image:: https://img.shields.io/badge/GitHub-insta--tweet-4f1abc
   :target: https://github.com/tdkorn/insta-tweet
   :alt: GitHub Repository

.. image:: https://static.pepy.tech/personalized-badge/insta-tweet?period=total&units=none&left_color=grey&right_color=blue&left_text=Downloads
    :target: https://pepy.tech/project/insta-tweet

.. image:: https://readthedocs.org/projects/instatweet/badge/?version=latest
    :target: https://instatweet.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


Automatically Repost Content From Instagram to Twitter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ever tried sharing an Instagram post to Twitter, only to find out that all you tweeted was a link, and not the actual photo/video?

.. image:: https://instatweet.readthedocs.io/en/latest/_images/share_with_instagram.png
    :alt: Sharing an Instagram post to Twitter directly from the Instagram app. Only a link appears.
        It could be literally anything, nobody will click it.


+-------------------------------------------------------------+
| ⚠ Humiliating 🤮                                            |
+=============================================================+
|  That could be literally anything. Nobody will click it.    |
+-------------------------------------------------------------+


|

|.InstaTweet|_ **shares the** *actual* **content of the post. Not just a link to it.**

|

.. image:: https://instatweet.readthedocs.io/en/latest/_images/share_with_instatweet.png
    :alt: Sharing an Instagram post to Twitter using InstaTweet. The actual photo or video appears in the tweet.
        It's a thicc cat, very handsome. Nobody will click the link, but they'll definitely see this bad boy.


With ``InstaTweet``, you can rest easy knowing that, although nobody will click the link,
they'll at least see what you posted.

...

What's InstaTweet?
~~~~~~~~~~~~~~~~~~~~~

|.InstaTweet|_ is a customizable tool to automatically repost content from Instagram to Twitter.



Simply create a |.Profile|_, configure the |mandatory-settings|_, and |.add_users|_ to repost from


.. code-block:: python

    from InstaTweet import Profile

    # Create a new (local) Profile
    >>> profile = Profile('myProfile')

    # Configure the mandatory settings (at minimum)
    >>> profile.twitter_keys = twitter_api_keys
    >>> profile.session_id = '6011991A'

    # Add at least one Instagram account to repost from
    >>> profile.add_users('the.dailykitten')

    # Save the Profile [optional]
    >>> profile.save()

    Saved Local Profile myProfile


Once configured, the |.Profile|_ can be used to initialize and |.start|_ InstaTweet:

.. code-block:: python

    from InstaTweet import InstaTweet

    # Directly initialize with a Profile object
    >>> insta_tweet = InstaTweet(profile)

    # Or load a saved Profile by name
    >>> insta_tweet = InstaTweet.load("myProfile")

    # Run InstaTweet by calling start()
    >>> insta_tweet.start()


|

.. image:: https://user-images.githubusercontent.com/96394652/232274766-71e87fb2-f402-466d-9624-f775d8e985ac.png

|

As ``InstaTweet`` runs, its progress will be logged to console:

.. code-block:: python

    Starting InstaTweet for Profile: myProfile
    Checking posts from @the.dailykitten
    
    Finished insta-tweeting for @the.dailykitten
    All users have been insta-tweeted

...

Okay... But Why? 😟
~~~~~~~~~~~~~~~~~~~~~~~


.. |why| replace:: 🐥 But Why? 🤨

+-----------------------------------------------------------------+
| |why|                                                           |
+=================================================================+
| **InstaTweet has two main use cases:**                          |
|                                                                 |
| * To automatically share your own Instagram posts to Twitter    |
| * To automatically tweet new content from other Instagram users |
|                                                                 |
| Regardless of your intention, InstaTweet will detect new posts  |
| from the users you specify, download them, and repost them to   |
| Twitter.                                                        |
+-----------------------------------------------------------------+


...


Other Use Case: The |.InstaClient|_
======================================

The package's custom |.InstaClient|_ can also be used as a standalone Instagram scraper

.. code-block:: python

   from InstaTweet import InstaClient

   >>> ig = InstaClient(session_id="kjfdn309wredsfl")
   >>> user = ig.get_user('dailykittenig')
   >>> print(user)

   <InstaTweet.instauser.InstaUser object at 0x000002B9A1101330>

   >>> print(user.posts)
   >>> ig.download_post(user.posts[0])

   [<InstaTweet.instapost.InstaPost object at 0x000002B9A250F5E0>, ...]
   Downloaded post https://www.instagram.com/p/Clht4NRrqRO by dailykittenig to C:\\path\\to\\insta-tweet\\downloads\\2981866202934977614.mp4

...

Installation
~~~~~~~~~~~~~~

To install using pip:

.. code-block:: shell

    pip install insta-tweet


Please note that ``InstaTweet`` requires ``Python >= 3.8``

...

Documentation
~~~~~~~~~~~~~~~~~

The rest of this `README <https://instatweet.readthedocs.io/en/latest/_readme/getting-started.html>`_,
the `API documentation <https://instatweet.readthedocs.io/en/latest/modules.html>`_, and
`snippets <https://instatweet.readthedocs.io/en/latest/snippets.html>`_
can all be found on `Read the Docs <https://instatweet.readthedocs.io/en/latest/index.html>`_


