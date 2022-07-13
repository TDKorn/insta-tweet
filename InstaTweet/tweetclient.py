from __future__ import annotations
import os
import random
import tweepy
import InstaTweet

from . import InstaPost
from typing import Union, Optional
from tweepy.errors import TweepyException


class TweetClient:

    MAX_HASHTAGS = 5
    DEFAULT_KEYS = {
        'Consumer Key': 'string',
        'Consumer Secret': 'string',
        'Access Token': 'string',
        'Token Secret': 'string'
    }

    def __init__(self, profile: InstaTweet.Profile, proxies: dict = None):
        """Initialize TweetClient using a profile

        Basically just a wrapper for tweepy. It uses the settings of a profile to initialize the API and send tweets

        :param profile: the profile to use when initializing a :class:`tweepy.API` object
        :param proxies: optional proxies to use (
        """
        self.profile = profile
        self.proxies = proxies
        self.api = self.get_api()

    def get_api(self) -> tweepy.API:
        """Initializes a :class:`tweepy.API` (Twitter API v1.1) using the current :class:`Profile`"""
        return tweepy.API(
            auth=self.get_oauth(self.profile.twitter_keys),
            user_agent=self.profile.user_agent,
            proxy=self.proxies
        )

    @staticmethod
    def get_oauth(api_keys: dict) -> tweepy.OAuth1UserHandler:
        if missing_keys := [key for key in TweetClient.DEFAULT_KEYS if key not in api_keys]:
            raise KeyError(
                f"Missing the following Twitter Keys: {missing_keys}"
            )
        if bad_keys := [key for key in TweetClient.DEFAULT_KEYS if not api_keys[key] or api_keys[key] == 'string']:
            raise ValueError(
                f"Invalid values for the following Twitter keys: {bad_keys}"
            )
        return tweepy.OAuth1UserHandler(
            consumer_key=api_keys['Consumer Key'],
            consumer_secret=api_keys['Consumer Secret'],
            access_token=api_keys['Access Token'],
            access_token_secret=api_keys['Token Secret']
        )

    def send_tweet(self, post: InstaPost, hashtags: Optional[list[str]] = None) -> bool:
        """Composes and sends a Tweet using an already-downloaded Instagram post

        :param post: the post to tweet; uses the :attr:`~.InstaPost.filepath` as media file source
        :param hashtags: a list of hashtags, from the :attr:`~.user_map`
            If non-empty, a few will randomly be chosen and included in the tweet
        """
        if not post.filepath or not os.path.exists(post.filepath):
            raise FileNotFoundError('Post must be downloaded first')

        if not (uploaded := self.upload_media(post)):
            return False

        try:
            tweet = self.api.update_status(
                status=self.build_tweet(post, hashtags),
                media_ids=[str(uploaded.media_id)],
            )
            print(f'Sent tweet for {post}')
            return post.add_tweet_data(tweet)

        except TweepyException as e:
            print('Failed to send tweet for {}:\nResponse: {}'.format(post, e))
            return False

    def upload_media(self, post: InstaPost) -> Union[tweepy.Media, bool]:
        """Uploads the media from an already-downloaded Instagram post to Twitter

        :param post: the Instagram post to use as the media source
        :return: the response from the Twitter API (if upload was successful) or ``False``
        """
        media = self.api.media_upload(
            filename=post.filepath,
            media_category='TWEET_VIDEO' if post.is_video else 'TWEET_IMAGE',
            wait_for_async_finalize=True,
            chunked=True
        )
        if media.processing_info['state'] != 'succeeded':
            print(f'Failed to upload media to Twitter for {post}')
            return False
        else:
            print(f'Successfully uploaded media to Twitter for {post}')
            return media

    def build_tweet(self, post: InstaPost, hashtags: Optional[list[str]] = None) -> str:
        """Uses an :class:`InstaPost` to build the body text of a tweet

        :param post: the post that's being tweeted; the caption and link are used
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
        """Randomly chooses hashtags from provided list, then returns them formatted as a string

        The qty chosen will either be 1 less than the length of the list (to avoid using the same ones in every tweet)
            or the value of :attr:`~.MAX_HASHTAGS`, whichever is smaller

        :param hashtags: a list of hashtags to randomly choose from and include in a tweet

        :Example:
            pick_hashtags(['cat','dog','woof']) -> '#woof #cat\n'

        :Note:
            A newline is included to make character counting easier for :meth:`~.build_tweet`

        """
        if not hashtags:
            return ''
        if not isinstance(hashtags, list):
            raise TypeError('Provide a list of hashtags')

        num_hashtags = min(len(hashtags) - 1, TweetClient.MAX_HASHTAGS)  # Pick at most MAX_HASHTAGS
        random_hashtags = random.sample(hashtags, max(1, num_hashtags))  # Pick at least 1

        return ' '.join(f'#{hashtag}' for hashtag in random_hashtags) + '\n'
