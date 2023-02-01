from __future__ import annotations

import os
import random
import InstaTweet

from tweepy import OAuth1UserHandler, API, Media, TweepyException
from typing import Union, Optional
from . import InstaPost


class TweetClient:

    MAX_HASHTAGS = 5
    DEFAULT_KEYS = {
        'Consumer Key': 'string',
        'Consumer Secret': 'string',
        'Access Token': 'string',
        'Token Secret': 'string'
    }

    def __init__(self, profile: InstaTweet.Profile, proxies: dict = None):
        """Initialize TweetClient using a :class:`~.Profile`

        Basically just a wrapper for tweepy.
        It uses the settings of a profile to initialize the API and send tweets

        :param profile: the profile to use when initializing a :class:`tweepy.API` object
        :param proxies: optional proxies to use when making API requests
        """
        self.profile = profile
        self.proxies = proxies
        self.api = self.get_api()

    def get_api(self) -> API:
        """Initializes a :class:`~.tweepy.API` object using the API keys of the loaded :class:`~.Profile`"""
        return API(
            auth=self.get_oauth(self.profile.twitter_keys),
            user_agent=self.profile.user_agent,
            proxy=self.proxies
        )

    @staticmethod
    def get_oauth(api_keys: dict) -> OAuth1UserHandler:
        """Initializes and returns an :class:`~.OAuth1UserHandler` object from tweepy using the specified API keys

        :param api_keys: Twitter developer API keys with v1.1 endpoint access
        """
        if missing_keys := [key for key in TweetClient.DEFAULT_KEYS if key not in api_keys]:
            raise KeyError(
                f"Missing the following Twitter Keys: {missing_keys}"
            )
        if bad_keys := [key for key in TweetClient.DEFAULT_KEYS if not api_keys[key] or api_keys[key] == 'string']:
            raise ValueError(
                f"Invalid values for the following Twitter keys: {bad_keys}"
            )
        return OAuth1UserHandler(
            consumer_key=api_keys['Consumer Key'],
            consumer_secret=api_keys['Consumer Secret'],
            access_token=api_keys['Access Token'],
            access_token_secret=api_keys['Token Secret']
        )

    def send_tweet(self, post: InstaPost, hashtags: Optional[list[str]] = None) -> bool:
        """Composes and sends a Tweet using an already-downloaded Instagram post

        .. admonition:: How Tweets are Sent
           :class: instatweet

           The :attr:`.InstaPost.filepath` -- set by :meth:`~.download_post` -- is used as the media source

           The body of the tweet is then generated by :meth:`~build_tweet`

        :param post: the post to tweet
        :param hashtags: a list of hashtags to randomly chose from and include in the tweet
        """
        if not post.is_downloaded:
            raise FileNotFoundError('Post must be downloaded first')

        media_ids = self.upload_media(post)
        if not isinstance(media_ids, list):
            return False

        try:
            tweet = self.api.update_status(
                status=self.build_tweet(post, hashtags),
                media_ids=media_ids,
            )
        except TweepyException as e:
            print('Failed to send tweet for {}:\nResponse: {}'.format(post, e))
            return False

        print(f'Sent tweet for {post}')
        return post.add_tweet_data(tweet)

    def upload_media(self, post: InstaPost) -> Union[list, bool]:
        """Uploads the media from an already-downloaded Instagram post to Twitter

        .. note:: If the post is a carousel, only the first 4 photos/videos will be uploaded

        :param post: the Instagram post to use as the media source
        :return: the list of uploaded media ids (if API upload was successful) or ``False``
        """
        if not post.is_downloaded:
            raise FileNotFoundError('Post must be downloaded first')

        content = post.children[:4] if post.is_carousel else [post]
        media_ids = []

        for media in content:
            media_upload = self.api.media_upload(
                filename=media.filepath,
                media_category='TWEET_VIDEO' if media.is_video else 'TWEET_IMAGE',
                wait_for_async_finalize=True,
                chunked=True)

            if hasattr(media_upload, 'processing_info'):
                if media_upload.processing_info['state'] != 'succeeded':
                    print(f'Failed to upload media to Twitter for {media}')
                    return False

            media_ids.append(str(media_upload.media_id))

        print(f'Successfully uploaded media to Twitter for {post}')
        return media_ids

    def build_tweet(self, post: InstaPost, hashtags: Optional[list[str]] = None) -> str:
        """Uses an :class:`~.InstaPost` to build the body text of a tweet

        .. admonition:: How Tweets are Composed
           :class: instatweet

           - The :attr:`~.InstaPost.caption` is used as a starting point
           - If you :meth:`~.add_hashtags` for the user, it will randomly :meth:`~pick_hashtags` to include
           - Lastly, the post's :attr:`~.InstaPost.permalink` is added to the end

        **Example**::

         >> post = instatweet.insta.get_user("dailykittenig").posts[0]
         >> tweet = instatweet.twitter.build_tweet(post)
         >> print(tweet)

         carousel support yuh
         #kitten #kittycat #catlover #petstagram #animals

         https://www.instagram.com/p/Cjl3UWBOd8k

        :param post: the post being tweeted
        :param hashtags: optional list of hashtags to randomly pick from and include
        :return: the text to use for the tweet
        """
        tags = self.pick_hashtags(hashtags)
        caption = post.caption.strip().replace('@', '@/')  # Avoid tagging randos on Twitter
        characters = 280 - len(tags) - len(post.permalink) - 2
        tweet = "{text}\n{hashtags}\n{link}".format(
            text=caption[:characters],
            hashtags=tags,
            link=post.permalink
        )
        return tweet

    @staticmethod
    def pick_hashtags(hashtags: list[str]) -> str:
        """Randomly picks hashtags from the provided list and returns them as a single string

        The number of hashtags chosen will either be 1 less than the length of the list (to avoid using the same tags
        in every tweet), or the value of :attr:`~.MAX_HASHTAGS`, whichever is smaller

        :param hashtags: a list of hashtags to randomly choose from

        :Example:

            ::

               from InstaTweet import TweetClient

               >> TweetClient.pick_hashtags(['cat','dog','woof'])
               "#woof #cat\\n"

        .. note:: A newline is added to help with formatting & character counting in :meth:`~.build_tweet`

        """
        if not hashtags:
            return ''
        if not isinstance(hashtags, list):
            raise TypeError('Provide a list of hashtags')

        num_hashtags = min(len(hashtags) - 1, TweetClient.MAX_HASHTAGS)  # Pick at most MAX_HASHTAGS
        random_hashtags = random.sample(hashtags, max(1, num_hashtags))  # Pick at least 1

        return ' '.join(f'#{hashtag}' for hashtag in random_hashtags) + '\n'
