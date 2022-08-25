InstaTweet - Automatically Repost Content From Instagram to Twitter
---------------------------------------------------------------------------

Ever tried sharing an Instagram post to Twitter, only to find out that all you tweeted was a link, and not the actual photo/video?

.. image:: https://instatweet.readthedocs.io/en/latest/_images/share_with_instagram.png
    :alt: Sharing an Instagram post to Twitter directly from the Instagram app. Only a link appears.
        It could be literally anything, nobody will click it.


.. admonition:: ‎ Humiliating 🤮
   :class: important-af

   That could be literally anything. Nobody will click it.



`InstaTweet <https://github.com/tdkorn/insta-tweet/blob/docs/InstaTweet/instatweet.py#L5-L142>`_ **shares the** *actual* **content of the post. Not just a link to it.**



.. image:: https://instatweet.readthedocs.io/en/latest/_images/share_with_instatweet.png
    :alt: Sharing an Instagram post to Twitter using InstaTweet. The actual photo or video appears in the tweet.
        It's a thicc cat, very handsome. Nobody will click the link, but they'll definitely see this bad boy.


With ``InstaTweet``, you can rest easy knowing that,
although nobody will click the link, they'll at least see what you posted.



What's InstaTweet?
~~~~~~~~~~~~~~~~~~~~~

`InstaTweet <https://github.com/tdkorn/insta-tweet/blob/docs/InstaTweet/instatweet.py#L5-L142>`_ is a customizable tool to automatically repost content from Instagram to Twitter.

Simply create a `Profile <https://github.com/tdkorn/insta-tweet/blob/docs/InstaTweet/profile.py#L12-L414>`_,
configure the `mandatory-settings <https://instatweet.readthedocs.io/en/latest/_readme/getting-started.html#mandatory-settings>`_,
and `add_users() <https://github.com/tdkorn/insta-tweet/blob/docs/InstaTweet/profile.py#L167-L197>`_ to repost from

.. code-block:: python

    from InstaTweet import Profile

    # Create a new (local) Profile
    >>> profile = Profile('myProfile')

    # Configure the required settings (at minimum)
    >>> profile.twitter_keys = twitter_api_keys
    >>> profile.session_id = '6011991A'

    # Add at least one Instagram account to repost from
    >>> profile.add_users('the.dailykitten')


Once configured, the `Profile <https://github.com/tdkorn/insta-tweet/blob/docs/InstaTweet/profile.py#L12-L414>`_ can be used to initialize and
`start() <https://github.com/tdkorn/insta-tweet/blob/docs/InstaTweet/instatweet.py#L73-L117>`_ an `InstaTweet <https://github.com/tdkorn/insta-tweet/blob/docs/InstaTweet/instatweet.py#L5-L142>`_ object

.. code-block:: python

    from InstaTweet import InstaTweet

    # Directly initialize with the Profile from above
    >>> insta_tweet = InstaTweet(profile)

    # Or, save the Profile...
    >>> profile.save()

    Saved Local Profile myProfile

    # ...then InstaTweet.load() the settings in (by Profile name)
    >>> insta_tweet = InstaTweet.load(profile_name="myProfile")

    # Run InstaTweet by calling start()
    >>> insta_tweet.start()


.. admonition:: From the Docs...
    :class: docs

    https://github.com/TDKorn/insta-tweet/blob/38016309bdce0fcfb8d91a0d3ea5a69af88faa3b/InstaTweet/instatweet.py#L73-L117


As ``InstaTweet`` runs, its progress will be logged to console:

.. code-block:: python

    Starting InstaTweet for Profile: myProfile
    Checking posts from @the.dailykitten
    ...
    Finished insta-tweeting for @the.dailykitten
    All users have been insta-tweeted


Okay... But Why? 😟
~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: But Why? 🤨
   :class: instatweet

   **InstaTweet has two main use cases:**

   * To automatically share your own Instagram posts to Twitter
   * To automatically tweet new content from other Instagram users

   Regardless of your intention, InstaTweet will detect new posts from the users you specify, download them, and repost
   them to Twitter.


Documentation
~~~~~~~~~~~~~~~~~

The rest of this `README <https://instatweet.readthedocs.io/en/latest/_readme/about-instatweet.html>`_,
extensive `API documentation <https://instatweet.readthedocs.io/en/latest/modules.html>`_, and
`snippets <https://instatweet.readthedocs.io/en/latest/snippets.html>`_
can all be found on `Read the Docs <https://instatweet.readthedocs.io/en/latest/index.html>`_

I put a lot of time into creating and (excessively) customizing the documentation for this package,
so it'd mean a lot to me if you could please continue reading there! 🥰



Installation
~~~~~~~~~~~~~~

To install using pip:

.. code-block:: shell

    pip install insta-tweet


Please note that ``InstaTweet`` requires ``Python >= 3.8``
