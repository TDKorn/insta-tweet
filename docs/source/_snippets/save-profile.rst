Saving a Profile
--------------------

.. admonition:: Saving a Profile
    :class: instatweet

    When you :meth:`~.save` your :class:`~.Profile`, the current :attr:`~.Profile.name`
    will be used to create or update a save file in the location specified by :attr:`~.local`

    .. admonition:: From the Docs...
        :class: docs

        .. autodata:: InstaTweet.profile.Profile.local
            :annotation: =True
            :noindex:


    * Local saves are made to the :attr:`~.LOCAL_DIR`, as pickle files
    * Remote saves are made to a database (via the :mod:`~.db` module) as pickle bytes


.. admonition:: Important!!
    :class: important-af

    **You MUST configure the** :attr:`~InstaTweet.db.DATABASE_URL` **environment variable to save/load remotely**

    InstaTweet uses ``SQLAlchemy`` to create a :class:`~.DBConnection`

    * Any ``SQLAlchemy``-supported database is therefore also supported by ``InstaTweet``
    * See the :mod:`~.db` module for more information