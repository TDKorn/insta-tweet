from __future__ import annotations
from abc import ABC, abstractmethod
from functools import cached_property
from typing import Dict, Optional, TYPE_CHECKING, List
from . import InstaPost

if TYPE_CHECKING:
    from . import InstaClient


class InstaPage(ABC):

    """Abstract wrapper class for wrapping API responses from Instagram pages"""

    def __init__(self, data: Dict, client: Optional[InstaClient] = None):
        """Initialize an :class:`InstaPage`

        Used to wrap responses from endpoints that contain Instagram post data,
        like Instagram user profiles and Instagram hashtag searches

        :param data: the API response JSON to use as source data
        :param client: the :class:`~.InstaClient` to use; required for :meth:`~.get_more_posts`
        """
        self.data = data
        self.client = client
        self._posts = []

    @abstractmethod
    def __str__(self) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the Instagram page"""
        pass

    @property
    @abstractmethod
    def page_data(self) -> Dict:
        """Data about the Instagram page itself"""
        pass

    @property
    @abstractmethod
    def media_data(self) -> Dict:
        """Data about posts on the Instagram page"""
        pass

    @property
    def id(self) -> int:
        """ID of the Instagram page"""
        return int(self.page_data.get('id', -1))

    @property
    def posts(self) -> List[InstaPost]:
        """Posts that have been scraped from the Instagram page

        To retrieve the next page of posts, call :meth:`get_more_posts`

        :returns: the page's posts as :class:`~.InstaPost` objects
        """
        if not self._posts:
            if edges := self.media_data.get('edges'):
                self._posts = [InstaPost(edge['node'], self.client) for edge in edges]
        return self._posts

    def get_more_posts(self) -> bool:
        """Requests the next page of posts from the :class:`InstaPage`

        If the page :attr:`~.has_more_posts`, they'll be added to the :attr:`~.posts` list

        :returns: ``True`` if the request was successful, otherwise ``False``
        """
        if not self.client:
            raise AttributeError("Must provide an InstaClient to scrape with")

        if not self.has_more_posts:
            print("All posts have already been scraped")
            return False

        if not (next_page := self._get_next_page()):
            print("Unable to retrieve the next page of posts")
            return False

        self.media_page_info.update(next_page.media_page_info)
        self._posts.extend(next_page.posts)
        return True

    @abstractmethod
    def _get_next_page(self) -> Optional[InstaPage]:
        """Makes the request for the next page of posts; wraps the response if successful"""
        pass

    @property
    def has_more_posts(self) -> bool:
        """Returns ``True`` if more posts can be scraped using :meth:`~.get_more_posts`"""
        return self.media_page_info.get('has_next_page')

    @property
    def end_cursor(self) -> str:
        """Cursor used in request by :meth:`~.get_more_posts`"""
        return self.media_page_info.get('end_cursor', '').strip('=')

    @property
    def media_page_info(self) -> Dict:
        return self.media_data.get('page_info', {})


class InstaUser(InstaPage):

    """API response wrapper for an Instagram user's profile"""

    def __init__(self, data: Dict, client: Optional[InstaClient] = None):
        """Initialize an :class:`InstaUser`

        :param data: the API response from :meth:`~.get_user`
        :param client: the :class:`~.InstaClient` to use
        """
        super().__init__(data, client)

    def __str__(self) -> str:
        return f"Instagram User: @{self.name}"

    @property
    def name(self) -> str:
        return self.page_data.get('username')

    @property
    def page_data(self) -> Dict:
        return self.data.get('data', {}).get('user', {})

    @property
    def media_data(self) -> Dict:
        return self.page_data.get('edge_owner_to_timeline_media', {'edges': []})

    def _get_next_page(self) -> Optional[InstaPage]:
        endpoint = 'https://www.instagram.com/graphql/query/?query_hash=8c2a529969ee035a5063f2fc8602a0fd' + \
                   f'&variables=%7B%22id%22%3A%22{self.id}%22%2C%22first%22%3A12%2C%22' + \
                   f'after%22%3A%22{self.end_cursor}%3D%3D%22%7D'
        response = self.client.request(endpoint)
        if not response.ok:
            return None
        try:
            return InstaUser(response.json())
        except Exception as e:
            raise RuntimeError('Failed to get more posts') from e


class Hashtag(InstaPage):

    """API response wrapper for an Instagram hashtag"""

    def __init__(self, data: Dict, client: Optional[InstaClient] = None):
        """Initialize a :class:`Hashtag`

        :param data: the API response from :meth:`~.get_hashtag`
        :param client: the :class:`~.InstaClient` to use
        """
        if (data := data.get('graphql', {}).get('hashtag')) is None:
            raise ValueError(f"Hashtag response data is missing")

        super().__init__(data, client)
        self._top_posts = []

    def __str__(self) -> str:
        return f"Instagram Hashtag: {self.name}"

    @property
    def name(self) -> str:
        return "#" + self.page_data.get('name')

    @property
    def page_data(self) -> Dict:
        return self.data

    @property
    def media_data(self) -> Dict:
        return self.page_data.get('edge_hashtag_to_media', {'count': 0, 'edges': []})

    @cached_property
    def top_posts(self) -> List[InstaPost]:
        return [InstaPost(edge['node'], self.client) for edge in self.top_media_data['edges']]

    @property
    def top_media_data(self) -> Dict:
        return self.page_data.get("edge_hashtag_to_top_posts", {"edges": []})

    def _get_next_page(self) -> Optional[InstaPage]:
        return self.client.get_hashtag(self.name, max_id=self.end_cursor)
