Viewing Profile Configuration
--------------------------------

The :class:`~.Profile` is a collection of configuration settings.


The :attr:`~.Profile.config` property can be called to create and return
a dictionary with all relevant settings

.. code-block:: python

   from InstaTweet import Profile

   >>> profile = Profile.load('myProfile')
   >>> print(profile.config)

   {'name': 'myProfile', 'local': True, 'session_id': '6011991A', 'twitter_keys': {'Consumer Key': 'string', 'Consumer Secret': 'string', 'Access Token': 'string', 'Token Secret': 'string'}, 'user_agent': 'Mozilla/5.0 (Linux; Android 9; GM1903 Build/PKQ1.190110.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36 Instagram 103.1.0.15.119 Android (28/9; 420dpi; 1080x2260; OnePlus; GM1903; OnePlus7; qcom; sv_SE; 164094539)', 'proxy_key': None, 'user_map': {}}


It's not the most legible though, and it hasn't even be fully configured yet.
A fully set up Profile would be even harder to read.

That why the the :meth:`~.view_config` method exists:

.. literalinclude:: ../../../InstaTweet/profile.py
   :pyobject: Profile.view_config
   :lines: 1-2,6-8
   :dedent:

.. _config-example:

.. admonition:: For Example...
   :class: example

   .. code-block:: python

      from InstaTweet import Profile

      >>> profile = Profile.load('myProfile')
      >>> profile.view_config()

      name : myProfile
      local : True
      session_id : 6011991A
      twitter_keys : {'Consumer Key': 'string', 'Consumer Secret': 'string', 'Access Token': 'string', 'Token Secret': 'string'}
      user_agent : Mozilla/5.0 (Linux; Android 9; GM1903 Build/PKQ1.190110.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36 Instagram 103.1.0.15.119 Android (28/9; 420dpi; 1080x2260; OnePlus; GM1903; OnePlus7; qcom; sv_SE; 164094539)
      proxy_key : None
      user_map : {}

