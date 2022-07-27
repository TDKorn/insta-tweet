InstaTweet Package
====================

Below, you'll find the documentation for each class/module in the  ``InstaTweet`` package.

.. admonition:: Just want to get started?
   :class: instatweet

   If don't care about the details and just want to get this running, I get you. All you really need to care about is the
   :class:`~.Profile` and :class:`~InstaTweet.instatweet.InstaTweet` classes,
   and maybe the :mod:`~.db` module


Otherwise, the other classes are pretty self explanatory



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



.. tip::
   * :class:`~.InstaClient` sends requests to Instagram
   * :class:`~.InstaPost` and :class:`~.InstaUser` wrap responses from Instagram
   * :class:`~.TweetClient` wraps the :class:`.tweepy.API` to :meth:`~.send_tweet` based off an :class:`~.InstaPost`
   * The :mod:`~.db` module contains the :class:`~.Profiles` database table and the :class:`~.DBConnection` class
