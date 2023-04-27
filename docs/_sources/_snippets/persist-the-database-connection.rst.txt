.. _Persist DBConnection:

Persisting The DBConnection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can assign a :meth:`~.DBConnection` to a variable if you want a persistent connection

Here's how:

.. code:: python

    from InstaTweet import DBConnection

    # When __enter__ is called for the first time, the engine is set
    >>> with DBConnection() as db:
    ...     pass

    # Since the database URL is constant,
    #__exit__() doesn't remove the ENGINE class var
    >>> print(db.ENGINE)
    Engine(postgresql://...)

    # The SESSION class var is cleared upon __exit__ though
    >>> print(db.SESSION)
    None


To connect to the database and create a new session, call :meth:`~.connect`
 It will persist until you somehow trigger a call to ``__exit__()``


.. code:: python

    # Using the DBConnection object from above
    # Call connect() to create a new connection
    >>> db.connect()

    # Now it can be used like a regular object, and the
    # connection will persist until you trigger a call to __exit__()
    >>> profile = db.load_profile('myProfile')
    >>> profile.view_config()

Output:

.. code:: shell

       name : myProfile
       local : True
       session_id :
       twitter_keys : {'Consumer Key': 'string', 'Consumer Secret': 'string', 'Access Token': 'string', 'Token Secret': 'string'}
       user_agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36
       proxy_key : None
       user_map : {}


yea