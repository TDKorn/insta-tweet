Running a Profile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once a :class:`~.Profile` is configured, it can be used to initialize and
:meth:`~.start` an :class:`~.InstaTweet` object


.. code-block:: python

    from InstaTweet import InstaTweet, Profile

    # Load an existing saved or unsaved profile into InstaTweet
    >>> profile = Profile.load("myProfile")
    >>> insta_tweet = InstaTweet(profile)

    # Or directly InstaTweet.load() the settings in by Profile name
    >>> insta_tweet = InstaTweet.load(profile_name="myProfile")

    # Then run InstaTweet by calling start()
    >>> insta_tweet.start()


.. admonition:: From the Docs...
    :class: docs

    .. automethod:: InstaTweet.instatweet.InstaTweet.start
        :noindex:


As ``InstaTweet`` runs, its progress will be logged to console:

.. code-block:: python

    Starting InstaTweet for Profile: myProfile
    Checking posts from @the.dailykitten
    ...
    Finished insta-tweeting for @the.dailykitten
    All users have been insta-tweeted

