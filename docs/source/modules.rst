InstaTweet Package
====================

Below, you'll find the documentation for each class/module in the  ``InstaTweet`` package.

.. toctree::
   :maxdepth: 2
   :caption: InstaTweet Package Contents

   instatweet_class
   profile
   db
   tweetclient
   instaclient
   instauser
   instapost
   utils


.. admonition:: Just want to get started?
   :class: instatweet

   If you don't care about the details and just want to get this running... I get you.

   You'll only need to be familiar with

   * The :class:`~.Profile`, which is used to configure all :ref:`settings <settings>`
   * The :class:`~InstaTweet.instatweet.InstaTweet` class, which is used to :meth:`~.start` the "main script"
   * The :mod:`~.db` module, but only if you plan to save data remotely



Otherwise, the other classes are pretty self explanatory

.. tip::

   * :class:`~.InstaClient` sends requests to Instagram
   * :class:`~.InstaPost` and :class:`~.InstaUser` wrap responses from Instagram
   * :class:`~.TweetClient` wraps the :class:`.tweepy.API` to :meth:`~.send_tweet` based off an :class:`~.InstaPost`
   * The :mod:`~.db` module contains the :class:`~.Profiles` database table and the :class:`~.DBConnection` class





