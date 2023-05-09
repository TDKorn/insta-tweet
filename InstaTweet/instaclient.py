import os
import requests
from requests import Response
from typing import Type, Union, Optional, Dict
from json.decoder import JSONDecodeError
from . import InstaPage, InstaUser, InstaPost, Hashtag


USER_AGENT = "Mozilla/5.0 (Linux; Android 9; GM1903 Build/PKQ1.190110.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36 Instagram 103.1.0.15.119 Android (28/9; 420dpi; 1080x2260; OnePlus; GM1903; OnePlus7; qcom; sv_SE; 164094539)"
"""Hardcoded user agent proven to work with the :meth:`~.InstaClient.get_user` endpoint
 
 :Version Added: ``v2.0.0b13``
 """


class InstaClient:

    """Minimalistic class for scraping/downloading Instagram user/media data"""

    DOWNLOAD_DIR = os.path.abspath('downloads')  #: [*Optional*] -- Directory to temporarily download media to

    def __init__(self, session_id: str, user_agent: str = USER_AGENT, proxies: Optional[Dict] = None):
        """Initialize an :class:`~InstaClient` with an Instagram sessionid cookie (at minimum)

        .. note:: As of v2.0.0b13, the endpoint used by :meth:`~get_user` seems to require a specific :attr:`~USER_AGENT`
           You can override the hardcoded one if you'd like, but you'll likely get a ``"useragent mismatch"`` response

        :param session_id: valid Instagram sessionid cookie from a browser
        :param user_agent: user agent to use in requests made by the class
        :param proxies: proxies to use in requests made by the class
        """
        if not isinstance(session_id, str):
            raise TypeError('session_id must be a string')

        self.session_id = session_id
        self.user_agent = user_agent
        self.proxies = proxies

        if not os.path.exists(InstaClient.DOWNLOAD_DIR):
            os.mkdir(InstaClient.DOWNLOAD_DIR)

    def request(self, url: str) -> requests.Response:
        """Sends a request using the :attr:`cookies`, :attr:`headers`, and :attr:`proxies`

        :param url: the Instagram URL to send the request to
        """
        return requests.get(
            url, headers=self.headers,
            cookies=self.cookies,
            proxies=self.proxies
        )

    def scrape(self, page: str) -> InstaPage:
        """Scrapes an Instagram page and wraps the response data

        :param page: an Instagram hashtag (prefixed with ``#``) or username
        :returns: an :class:`~.InstaUser` or :class:`~.Hashtag`
        """
        if isinstance(page, str):
            if page.startswith("#"):
                return self.get_hashtag(page)
            return self.get_user(page)
        raise TypeError(f"`page` must be of type {str}")

    def get_hashtag(self, tag: str, max_id: str = '') -> Hashtag:
        """Scrapes an Instagram hashtag and wraps the response with :class:`~.Hashtag`

        :param tag: the hashtag to scrape (with or without a ``#``)
        :param max_id: the end cursor
        """
        tag = tag.lstrip("#")
        endpoint = f'https://www.instagram.com/explore/tags/{tag}/?__a=1&max_id={max_id}&__d=dis'
        response = self.request(endpoint)
        return self._wrap(tag, response, Hashtag)

    def get_user(self, username: str) -> InstaUser:
        """Scrapes an Instagram user's profile and wraps the response with :class:`~.InstaUser`

        :param username: the username of the IG user to scrape
        """
        username = username.lstrip('@')
        endpoint = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
        response = self.request(endpoint)
        return self._wrap(username, response, InstaUser)

    def _wrap(self, page: str, response: Response, Wrapper: Type[InstaPage]) -> InstaPage:
        """Validates and wraps the API response from an Instagram page
        """
        page = f'user @{page}' if Wrapper is InstaUser else f'hashtag #{page}'
        if response.ok:
            try:
                return Wrapper(response.json(), self)
            except JSONDecodeError as e:
                raise RuntimeError(f'Unable to scrape Instagram {page}') from e
        else:
            try:
                error = response.json()
            except JSONDecodeError:
                error = response.reason
            raise RuntimeError(
                'Failed to scrape Instagram {page}\nResponse: [{code}] -- {e}'.format(
                    page=page, code=response.status_code, e=error
                )
            )

    def get_username(self, user_id: Union[int, str]) -> str:
        """Retrieves the Instagram username for the user with the provided ``user_id``

        .. tip:: Use this with :meth:`get_user` to scrape by ``user_id``::

           >> user_id = 51276430399
           >> username = insta.get_username(user_id)
           >> user = insta.get_user(username)
           >> print(user.posts[0])

           Post 2981866202934977614 by @dailykittenig on 2022-11-29 01:44:37

        :param user_id: the id of the Instagram user to retrieve the username of
        """
        endpoint = f"https://i.instagram.com/api/v1/users/{user_id}/info"
        response = self.request(endpoint)
        if response.ok:
            return response.json().get('user', {}).get('username', '')
        else:
            raise RuntimeError(f"Failed to retrieve info for Instagram user with id {user_id}")

    def download_post(self, post: InstaPost, filepath: Optional[str] = None) -> bool:
        """Downloads the media from an Instagram post

        :param post: the :class:`~.InstaPost` of the post to download
        :param filepath: the path to save the downloaded media; if ``None``, saves to the :attr:`~DOWNLOAD_DIR`
        """
        if post.is_carousel:
            for child in post.children:
                self.download_post(child)
            return post.is_downloaded

        response = self.request(post.media_url)
        if not response.ok:
            print(f'Failed to download post {post.permalink} by {post.owner["username"]}')
            return False

        filepath = filepath if filepath else os.path.join(self.DOWNLOAD_DIR, post.filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f'Downloaded post {post.permalink} by {post.owner["username"]} to {filepath}')
        post.filepath = filepath
        return True

    @property
    def headers(self) -> Dict:
        """Headers to use in :meth:`~.request`"""
        return {'User-Agent': self.user_agent, }

    @property
    def cookies(self) -> Dict:
        """Cookies to use in :meth:`~.request`"""
        return {'sessionid': self.session_id, }
