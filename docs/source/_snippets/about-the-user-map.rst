.. _About the User Map:

About the User Map
--------------------

.. admonition:: About the User Map
    :class: instatweet

    The :attr:`~.user_map` is a dict containing info about the users added to a :class:`~.Profile`

    * It's used to help detect new posts and compose tweets on a per-user basis
    * Entries are created when you :meth:`~.add_users`, which map the user to a :attr:`~.USER_MAPPING`
    * The :attr:`~.USER_MAPPING` maintains lists of hashtags, scraped posts, and sent tweets
    * The mapping is updated when you :meth:`~.add_hashtags` and successfully :meth:`~.send_tweet`

    You can access entries in the :attr:`~.user_map` as follows:

    * :meth:`~.Profile.get_user` allows you to retrieve a full entry by username
    * :meth:`~.get_hashtags_for`, :meth:`.get_scraped_from`, :meth:`.get_tweets_for` provide access
      to lists
