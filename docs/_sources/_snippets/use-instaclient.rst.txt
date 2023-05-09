.. _use-instaclient:

Other Use Case: The :class:`~.InstaClient`
======================================================

The package's custom :class:`~.InstaClient` can be used separately to scrape Instagram

.. code-block:: python

   from InstaTweet import InstaClient

   >>> ig = InstaClient(session_id="kjfdn309wredsfl")

   # Scrape Instagram user or hashtag
   >>> user = ig.get_user('dailykittenig')
   >>> hashtag = ig.get_hashtag('#dailykitten')
   >>> print(user, hashtag, sep='\n')

   Instagram User: @dailykittenig
   Instagram Hashtag: #dailykitten

   # Download most recent post
   >>> post = user.posts[0]
   >>> print(post)
   >>> ig.download_post(post)

   Post 2981866202934977614 by @dailykittenig on 2022-11-29 01:44:37
   Downloaded post https://www.instagram.com/p/Clht4NRrqRO by dailykittenig to C:\path\to\insta-tweet\downloads\2981866202934977614.mp4


