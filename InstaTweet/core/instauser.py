from . import InstaPost


class InstaUser(object):
    """Convenience wrapper for Instagram profile API response"""

    def __init__(self, user_json):
        self.json = user_json

    @property
    def user_data(self):
        return self.json.get('graphql', {}).get('user')

    @property
    def id(self):
        return int(self.user_data.get('id'))

    @property
    def media_data(self):
        return self.user_data.get('edge_owner_to_timeline_media', {'edges': []})

    @property
    def posts(self):
        return [InstaPost(media['node']) for media in self.media_data['edges']]
