from datetime import datetime


class InstaPost(object):

    def __init__(self, post_data):
        """Convenience wrapper for Instagram media data"""
        self.json = post_data
        self.id = post_data['id']  # Something's wrong if this raises an error
        self.shortcode = post_data.get('shortcode', '')
        self.permalink = f'https://www.instagram.com/p/{self.shortcode}'
        self.timestamp = datetime.utcfromtimestamp(self.json.get('taken_at_timestamp', ''))
        self.is_video = self.json.get('is_video', False)
        self.is_carousel = bool(self.json.get('edge_sidecar_to_children', False))
        self.video_url = post_data.get('video_url', '')
        self.photo_url = post_data.get('display_url',
                                       post_data.get('thumbnail_src',
                                                     post_data.get('thumbnail_resources', [{}])[-1].get('src', '')))
        self.owner = {'username': None, 'id': None}
        self.dimensions = {'height': None, 'width': None}

        self.owner.update(self.json.get('owner', {}))
        self.dimensions.update(self.json.get('dimensions', {}))

    def __str__(self):
        return f'Post {self.id} by @{self.owner["username"]} on {str(self.timestamp)}'

    @property
    def media_url(self):
        return self.video_url if self.is_video else self.photo_url

    @property
    def caption(self):
        if caption_node := self.json.get('edge_media_to_caption', {}).get('edges', [{}]):
            return caption_node[0].get('node', {}).get('text', '')
        return ''
