The ``db`` module
~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: InstaTweet.db
   :exclude-members: DATABASE_URL, Profiles, DBConnection

..
   Automodule above allows for :mod: references to db module and places link target at the top


The :mod:`~.db` module contains the :class:`~.DBConnection` class and the :class:`~.Profiles` database table

.. admonition:: The Database Table
    :class: example

    In the :class:`~.Profiles` database table each row corresponds to a unique :class:`~.Profile`

    The table only has two fields per row:
        * :attr:`~.Profiles.name`: primary key for lookups/insertions
        * :attr:`~.Profiles.config`: stores the Profile as pickle bytes via :meth:`~.to_pickle`


.. admonition:: How is profile data saved to the database?
    :class: instatweet

    When a :class:`~.Profile` calls :meth:`~.Profile.save` and has :attr:`~.Profile.local` ``= False``, it will
    :meth:`~.connect` to the database specified by the :attr:`~.DABATASE_URL` environment variable and use it
    to :meth:`~.query_profile` settings

    * If the :meth:`~.profile_exists` in the database already, its :attr:`~.Profiles.config` data will be updated
    * Otherwise, the :class:`DBConnection` will :meth:`~.save_profile` data in a new table row

.. admonition:: Important!!
    :class: important-af

    **You MUST configure the** :attr:`~InstaTweet.db.DATABASE_URL` **environment variable to save/load remotely**

    * InstaTweet uses ``SQLAlchemy`` to create a :class:`~.DBConnection` -- any db it supports is compatible
    * See the :mod:`~.db` module for more information


.. admonition:: One Last Thing!
    :class: shut-up

    The :class:`~.DBConnection` is meant to be used as a context manager

    .. code-block:: python

        with DBConnection() as db:
            # Do Something

    - A :attr:`~SESSION` is created/destroyed when saving, loading, and InstaTweeting a :class:`~.Profile`

    If you don't want that, here's instructions on :ref:`Persist DBConnection`

...

.. autodata:: InstaTweet.db.DATABASE_URL
   :annotation:

...

.. autoclass:: InstaTweet.db.Profiles
   :exclude-members: __init__

   .. autoattribute:: InstaTweet.db.Profiles.name
    :annotation:

   .. autoattribute:: InstaTweet.db.Profiles.config
    :annotation:

...

.. autoclass:: InstaTweet.db.DBConnection
    :members:
    :exclude-members: SESSION, ENGINE

    .. autoattribute:: InstaTweet.db.DBConnection.SESSION
     :annotation:

    .. autoattribute:: InstaTweet.db.DBConnection.ENGINE
     :annotation:



