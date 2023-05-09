.. _about-page-map:
About the Page Map
~~~~~~~~~~~~~~~~~~~

.. admonition:: About the Page Map
    :class: instatweet

    **The** :attr:`~.page_map` **is a dict containing info about the pages added to a** :class:`~.Profile`

    * It's used to help detect new posts and compose tweets on a per-page basis
    * Entries are created when you :meth:`~.add_pages`, which map the page to a :attr:`~.PAGE_MAPPING`
    * The :attr:`~.PAGE_MAPPING` maintains lists of hashtags, scraped posts, and sent tweets
    * The mapping is updated when you :meth:`~.add_hashtags` and successfully :meth:`~.send_tweet`

    **You can access entries in the** :attr:`~.page_map` **as follows:**

    * :meth:`~.Profile.get_page` allows you to retrieve a full entry by page name
    * :meth:`~.get_hashtags_for`, :meth:`.get_scraped_from`, :meth:`.get_tweets_for` provide access
      to lists
