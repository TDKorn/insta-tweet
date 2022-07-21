The ``db`` module
-----------------------------------

The :mod:`~.db` module contains the :class:`~.DBConnection` class as well as the :class:`~.Profiles` database table

* Each row of the database will correspond to a unique :class:`~.Profile`
* The :attr:`.Profile.name` will be used as the primary key for lookups/insertions


When a :class:`~.Profile` calls :meth:`~.Profile.save` and has :attr:`~.Profile.local` ``= False``, the database is
queried by its :attr:`~.Profile.name`

* If an existing save is found, it will be updated with the new pickled data
* Otherwise, a new row will be inserted and the settings will be saved there

...

**Please Note**

* ``InstaTweet`` is compatible with any database that can be connected to using ``SQLAlchemy``
* The :class:`~.DBConnection` is meant to be used as a context manager

  - It will create/destroy a session when saving, loading, and InstaTweeting a :class:`~.Profile`
  - If desired, a persistent connection can be created and used instead

...

.. automodule:: InstaTweet.db
   :members:
   :undoc-members:
   :show-inheritance:
