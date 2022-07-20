import os
from datetime import datetime
from tweepy.models import Status


class InstaPost:

    """Minimalistic API response wrapper for an Instagram post"""

    def __init__(self, post_data: dict):
        """Initialize an :class:`~InstaPost`

        :param post_data: the JSON response data of an Instagram post -- found within auser's profile data
        """
        self.json = post_data
        self.id = post_data['id']  # Something's wrong if this raises an error
        self.is_video = post_data.get('is_video', False)
        self.video_url = post_data.get('video_url', '')
        self.dimensions = post_data.get('dimensions', {})
        # Attributes set by other classes
        self.filepath = ''    # Set by InstaClient when downloaded
        self.tweet_data = None  # Set by TweetClient when tweeted

    def __str__(self):
        return f'Post {self.id} by @{self.owner["username"]} on {self.timestamp}'

    @property
    def filename(self) -> str:
        """Default filepath basename to use when downloading the post (:attr:`~id` + :attr:`~filetype`)"""
        return self.id + self.filetype

    @property
    def filetype(self) -> str:
        """Filetype of the post, based on the value of :attr:`~is_video`"""
        return 'mp4' if self.is_video else 'jpg'

    @property
    def is_downloaded(self) -> bool:
        """Checks if the post has been downloaded yet (``filepath`` attribute is set by :class:`~.InstaClient`)"""
        return os.path.exists(self.filepath)

    @property
    def owner(self):
        if owner := self.json.get('owner', self.json.get('user', {})):
            return owner
        return dict.fromkeys(['id', 'username'])

    @property
    def is_carousel(self):
        return self.json.get('media_type') == 8

    @property
    def shortcode(self):
        return self.json.get('shortcode', self.json.get('code', ''))

    @property
    def permalink(self):
        return f'https://www.instagram.com/p/{self.shortcode}'

    @property
    def thumbnail_url(self):
        return self.json.get('display_url',
                             self.json.get('thumbnail_src',
                                           self.json.get('thumbnail_resources',
                                                         [{}])[-1].get('src', '')))

    @property
    def timestamp(self):
        if timestamp := self.json.get('taken_at_timestamp', self.json.get('taken_at', '')):
            return datetime.utcfromtimestamp(timestamp)
        return ''

    @property
    def media_url(self):
        return self.video_url if self.is_video else self.thumbnail_url

    @property
    def caption(self):
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
