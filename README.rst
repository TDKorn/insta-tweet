.. meta::
   :title: InstaTweet - Automatically Repost Content From Instagram to Twitter
   :description: A Python package to automatically repost content from Instagram to Twitter

.. |.InstaTweet| replace:: ``InstaTweet``
.. _.InstaTweet: https://github.com/tdkorn/insta-tweet/blob/master/InstaTweet/instatweet.py#L5-L147
.. |.add_pages| replace:: ``add_pages()``
.. _.add_pages: https://github.com/tdkorn/insta-tweet/blob/master/InstaTweet/profile.py#L132-L165
.. |.Profile| replace:: ``Profile``
.. _.Profile: https://github.com/tdkorn/insta-tweet/blob/master/InstaTweet/profile.py#L11-L382
.. |.start| replace:: ``start()``
.. _.start: https://github.com/tdkorn/insta-tweet/blob/master/InstaTweet/instatweet.py#L71-L121
.. |.InstaClient| replace:: ``InstaClient``
.. _.InstaClient: https://github.com/tdkorn/insta-tweet/blob/master/InstaTweet/instaclient.py#L16-L159
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


.. raw:: html

   <table>
      <tr align="left">
         <th>⚠ Humiliating 🤮</th>
      </tr>
      <tr>
         <td>


That could be literally anything. Nobody will click it.

.. raw:: html

   </td></tr>
   </table>

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



Simply create a |.Profile|_, configure the |mandatory-settings|_, and |.add_pages|_ to repost from


.. code-block:: python

    from InstaTweet import Profile

    # Create a new (local) Profile
    >>> profile = Profile('myProfile')

    # Configure the mandatory settings (at minimum)
    >>> profile.twitter_keys = twitter_api_keys
    >>> profile.session_id = '6011991A'

    # Add at least one Instagram page (user/hashtag) to repost from
    >>> profile.add_pages(['the.dailykitten', '#thedailykitten'])

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

.. image:: https://user-images.githubusercontent.com/96394652/236979506-83d12d6f-114d-43ce-b4db-b062f8d0ed3a.png
   :width: 700px

|

As ``InstaTweet`` runs, its progress will be logged to console:

.. code-block:: python

    Starting InstaTweet for Profile: myProfile
    Checking posts from @the.dailykitten
    ...
    Checking posts from #thedailykitten
    ...
    Finished insta-tweeting for #thedailykitten
    All pages have been insta-tweeted

...

Okay... But Why? 😟
~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

   <table>
      <tr align="left">
         <th>🐥 But Why? 🤨</th>
      </tr>
      <tr>
         <td>

**InstaTweet has two main use cases:**

* To automatically share your own Instagram posts to Twitter
* To automatically tweet new content from other Instagram users/hashtags

Regardless of your intention, InstaTweet will detect new posts from the pages you specify,
download them, and repost them to Twitter.

.. raw:: html

   </td></tr>
   </table>


...


Other Use Case: The |.InstaClient|_
======================================

The package's custom |.InstaClient|_ can also be used as a standalone Instagram scraper

.. code-block:: python

   from InstaTweet import InstaClient

   >>> ig = InstaClient(session_id="kjfdn309wredsfl")

   # Scrape Instagram user or hashtag
   >>> user = ig.get_user('dailykittenig')
   >>> hashtag = ig.get_hashtag('#dailykitten')
   >>> print(user, hashtag, sep='\n')

   Instagram User: @dailykittenig
   Instagram Hashtag: #dailykitten

   # Download most recent post
   >>> post = user.posts[0]
   >>> print(post)
   >>> ig.download_post(post)

   Post 2981866202934977614 by @dailykittenig on 2022-11-29 01:44:37
   Downloaded post https://www.instagram.com/p/Clht4NRrqRO by dailykittenig to C:\path\to\insta-tweet\downloads\2981866202934977614.mp4

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


