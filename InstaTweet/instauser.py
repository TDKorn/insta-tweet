from __future__ import annotations
from . import InstaPost


class InstaUser:
    """Minimalistic API response wrapper for an Instagram profile"""

    def __init__(self, data: dict, client: "InstaClient" = None):
        """Initialize an :class:`InstaUser`

        :param data: the API response JSON to use as source data
        :param client: API client to use; only required for :meth:`~.get_more_posts`
        """
        self.json = data
        self.client = client
        self._posts = []

    @property
    def id(self) -> int:
        """Instagram User ID"""
        return int(self.user_data.get('id', -1))

    @property
    def posts(self) -> [InstaPost]:
        """Returns the list of posts scraped from the Instagram user"""
        if not self._posts:
            if edges := self.media_data.get('edges'):
                self._posts = [InstaPost(edge['node']) for edge in edges]
        return self._posts

    @property
    def media_data(self) -> dict:
        return self.user_data.get('edge_owner_to_timeline_media', {'edges': []})

    @property
    def user_data(self) -> dict:
        return self.json.get('data', {}).get('user', {})

    def get_more_posts(self) -> bool:
        """Requests the next page of posts

        If the user :attr:`~.has_more_posts`, they'll be added to the :attr:`~.posts` list

        :returns: ``True`` if the request was successful, otherwise ``False``
        """
        if not self.has_more_posts:
            print("All posts have already been scraped")
            return False

        if not self.client:
            raise AttributeError("InstaClient is required to request more posts")

        endpoint = 'https://www.instagram.com/graphql/query/?query_hash=8c2a529969ee035a5063f2fc8602a0fd' + \
                   f'&variables=%7B%22id%22%3A%22{self.id}%22%2C%22first%22%3A12%2C%22' + \
                   f'after%22%3A%22{self.end_cursor}%3D%3D%22%7D'
        response = self.client.request(endpoint)
        if not response.ok:
            return False

        try:
            u = InstaUser(response.json())
        except Exception as e:
            raise RuntimeError('Failed to get more posts') from e

        self.page_info.update(u.page_info)
        self._posts.extend(u.posts)
        return True

    @property
    def has_more_posts(self) -> bool:
        """Returns ``True`` if more posts can be scraped using :meth:`~.get_more_posts`"""
        return self.page_info.get('has_next_page')

    @property
    def end_cursor(self) -> str:
        """Cursor used in request by :meth:`~.get_more_posts`"""
        return self.page_info.get('end_cursor', '').strip('=')

    @property
    def page_info(self) -> dict:
        return self.media_data.get('page_info', {})
