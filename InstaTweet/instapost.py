import os
from typing import Union
from datetime import datetime
from tweepy.models import Status


class InstaPost:

    """Minimalistic API response wrapper for an Instagram post"""

    def __init__(self, post_data: dict):
        """Initialize an :class:`~InstaPost`

        :param post_data: the JSON response data of a single Instagram post, found within the :attr:`~.InstaUser.user_data`
        """
        self.json = post_data
        self.id = post_data['id']  #: The post id
        self.is_video = post_data.get('is_video', False)  #: Indicates if the post is a video or photo
        self.video_url = post_data.get('video_url', '')
        self.dimensions = post_data.get('dimensions', {})
        # Attributes set by other classes
        self.filepath = ''      #:``str``: Path of downloaded media, set by :meth:`~.InstaClient.download_post`
        self.tweet_data = None  #:``dict``: Limited data from a successful tweet based off this post, set by :meth:`~.TweetClient.send_tweet`

    def __str__(self):
        return f'Post {self.id} by @{self.owner["username"]} on {self.timestamp}'

    @property
    def filename(self) -> str:
        """Concatenates :attr:`~id` + :attr:`~filetype` to create the default filename, for use when saving the post

        :For Example:::

           >> print(post.filename)
           "2868062811604347946.mp4"

        """
        return self.id + self.filetype

    @property
    def filetype(self) -> str:
        """Filetype of the post, based on the value of :attr:`~is_video`"""
        return 'mp4' if self.is_video else 'jpg'

    @property
    def is_downloaded(self) -> bool:
        """Checks the :attr:`~filepath` to see if the post has been downloaded yet"""
        return os.path.exists(self.filepath)

    @property
    def owner(self) -> dict:
        if owner := self.json.get('owner', self.json.get('user', {})):
            return owner
        return dict.fromkeys(['id', 'username'])

    @property
    def is_carousel(self) -> bool:
        return self.json.get('media_type') == 8

    @property
    def shortcode(self) -> str:
        return self.json.get('shortcode', self.json.get('code', ''))

    @property
    def permalink(self) -> str:
        return f'https://www.instagram.com/p/{self.shortcode}'

    @property
    def thumbnail_url(self) -> str:
        return self.json.get('display_url',
                             self.json.get('thumbnail_src',
                                           self.json.get('thumbnail_resources',
                                                         [{}])[-1].get('src', '')))

    @property
    def timestamp(self) -> Union[datetime, str]:
        if timestamp := self.json.get('taken_at_timestamp', self.json.get('taken_at', '')):
            return datetime.utcfromtimestamp(timestamp)
        return ''

    @property
    def media_url(self) -> str:
        """The direct URL to the actual post content

        :returns: the :attr:`~video_url` if the post is a video, otherwise the :attr:`~thumbnail_url`
        """
        return self.video_url if self.is_video else self.thumbnail_url

    @property
    def caption(self) -> str:
        if caption_edge := self.json.get('edge_media_to_caption', {}).get('edges', []):
            return caption_edge[0].get('node', {}).get('text', '')
        return ''

    def add_tweet_data(self, tweet: Status) -> bool:
        """Used by :class:`~.TweetClient` to add minimal tweet data after the post has been tweeted

        :param tweet: a :class:`~tweepy.models.Status` object from a successfully sent tweet
        """
        self.tweet_data = {
            'link': tweet.entities['urls'][0]['url'],
            'created_at': str(tweet.created_at),
            'text': tweet.text
        }
        return True
