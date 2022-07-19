from . import InstaPost


class InstaUser:
    """Minimalistic API response wrapper for an Instagram profile"""

    def __init__(self, data: dict):
        """Initialize an :class:`InstaUser`

        :param data: the API response JSON to use as source data
        """
        self.json = data

    @property
    def user_data(self):
        return self.json.get('graphql', {}).get('user')

    @property
    def media_data(self):
        return self.user_data.get('edge_owner_to_timeline_media', {'edges': []})

    @property
    def posts(self):
        return [InstaPost(media['node']) for media in self.media_data['edges']]

    @property
    def id(self):
        return int(self.user_data.get('id', -1))