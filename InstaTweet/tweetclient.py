import os
import tweepy
from typing import Union
from InstaTweet import InstaPost
from tweepy.errors import TweepyException


class TweetClient:

    DEFAULT_KEYS = {
        'Consumer Key': 'string',
        'Consumer Secret': 'string',
        'Access Token': 'string',
        'Token Secret': 'string'
    }

    def __init__(self, profile, proxies=None):
        self.profile = profile
        self.proxies = proxies
        self.api = self.get_api()

    @staticmethod
    def get_oauth(api_keys: dict):
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

    def get_api(self):
        return tweepy.API(
            auth=self.get_oauth(self.profile),
            user_agent=self.profile.user_agent,
            proxy=self.proxies
        )

    def send_tweet(self, post: InstaPost, hashtags: list[str]) -> bool:
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
                status=self.build_tweet(post),
                media_ids=[str(uploaded.media_id)],
            )
            return post.add_tweet_data(tweet)

        except TweepyException as e:
            print('Failed to update status:\nResponse: {}'.format(e))
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

    def build_tweet(self, post: InstaPost):
        characters = 295 - len(post.permalink)
        caption = post.caption.strip().replace('@', '@/')  # Avoid tagging randos on Twitter
        tweet = "{text}\n\n{link}".format(
            text=caption[:characters],
            link=post.permalink
        )
        return tweet
