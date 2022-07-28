The ``db`` module
-----------------------------------

The :mod:`~.db` module contains the :class:`~.DBConnection` class as well as the :class:`~.Profiles` database table

* Each row of the database will correspond to a unique :class:`~.Profile`
* The :attr:`.Profile.name` will be used as the primary key for lookups/insertions


When a :class:`~.Profile` calls :meth:`~.Profile.save` and has :attr:`~.Profile.local` ``= False``, the database will
be queried

* If an existing database row is found for the  :attr:`~.Profile.name`, the save data will be updated
* Otherwise, a new row will be inserted and the settings will be saved there

...

**Please Note**

* ``InstaTweet`` is compatible with any database that can be connected to using ``SQLAlchemy``
* The :class:`~.DBConnection` is meant to be used as a context manager

  - It will create/destroy a session when saving, loading, and InstaTweeting a :class:`~.Profile`
  - If desired, a persistent connection can be created and used instead


.. automodule:: InstaTweet.db
   :exclude-members: DATABASE_URL, Profiles, DBConnection

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



