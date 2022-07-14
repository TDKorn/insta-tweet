from __future__ import annotations
from datetime import datetime


class InstaPost:

    def __init__(self, post_data):
        """Convenience wrapper for Instagram media data"""
        self.json = post_data
        self.id = post_data['id']  # Something's wrong if this raises an error
        self.is_video = self.json.get('is_video', False)
        self.video_url = self.json.get('video_url', '')
        self.dimensions = self.json.get('dimensions', {})

        self.filepath = None    # Will be set when downloaded
        self.tweet_data = None  # Will be set when tweeted

    def __str__(self):
        return f'Post {self.id} by @{self.owner["username"]} on {self.timestamp}'

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

    def add_tweet_data(self, tweet: "tweepy.models.Status"):
        self.tweet_data = {
            'link': tweet.entities['urls'][0]['url'],
            'created_at': str(tweet.created_at),
            'text': tweet.text
        }
        return True
