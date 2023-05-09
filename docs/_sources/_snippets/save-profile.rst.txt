.. _save-profile:

Saving a Profile
~~~~~~~~~~~~~~~~~~

.. admonition:: Saving a Profile
    :class: instatweet

    When you :meth:`~.save` your :class:`~.Profile`, the current or specified :attr:`~.Profile.name`
    will be used to create or update a save file in the location specified by :attr:`~.local`

    .. admonition:: From the Docs...
        :class: docs

        .. automethod:: InstaTweet.profile.Profile.save
            :noindex:

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


Example: Save a Profile
========================

.. note:: You can specify a new :attr:`~.Profile.name`
   for the profile in the call to :meth:`~.save`

.. code-block:: python

    from InstaTweet import Profile

    >>> p = Profile('myProfile')
    >>> p.save()

    Saved Local Profile myProfile

    >>> p.save('aProfile')
    >>> print(p.name)

    Saved Local Profile aProfile
    aProfile

Profile names must be unique - you cannot save or create a profile if a
:meth:`~.profile_exists` with that name already

.. code-block:: python

    >>> q = Profile('myProfile')

    FileExistsError: Local save file already exists for profile named "myProfile"
    Please choose another name, load the profile, or delete the file.

