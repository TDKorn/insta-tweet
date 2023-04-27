.. _use-instaclient:

Other Use Case: The :class:`~.InstaClient`
======================================================

The package's custom :class:`~.InstaClient` can be used separately to scrape Instagram

.. code-block:: python

   from InstaTweet import InstaClient

   >>> ig = InstaClient(session_id="kjfdn309wredsfl")
   >>> user = ig.get_user('dailykittenig')
   >>> print(user)

   <InstaTweet.instauser.InstaUser object at 0x000002B9A1101330>

   >>> print(user.posts)
   >>> ig.download_post(user.posts[0])

   [<InstaTweet.instapost.InstaPost object at 0x000002B9A250F5E0>, ...]
   Downloaded post https://www.instagram.com/p/Clht4NRrqRO by dailykittenig to C:\\path\\to\\insta-tweet\\downloads\\2981866202934977614.mp4


