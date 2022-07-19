import os
import requests
from json.decoder import JSONDecodeError
from . import InstaUser, InstaPost, utils


class InstaClient:

    """Minimalistic class for scraping/downloading Instagram user/media data"""

    DOWNLOAD_DIR = os.path.abspath('downloads')

    def __init__(self, session_id: str, user_agent: str = None, proxies: dict = None):
        """Initialize an :class:`~InstaClient` with a sessionid cookie (at minimum)

        :param session_id: valid Instagram sessionid cookie from a browser
        :param user_agent: user agent to use in requests made by the class
        """
        if not isinstance(session_id, str):
            raise TypeError('session_id must be a string')

        self.session_id = session_id
        self.user_agent = user_agent if user_agent else utils.get_agent()
        self.proxies = proxies

        if not os.path.exists(InstaClient.DOWNLOAD_DIR):
            os.mkdir(InstaClient.DOWNLOAD_DIR)

    def request(self, url: str) -> requests.Response:
        """Sends a request using the :attr:`cookies`, :attr:`headers`, and :ivar:`proxies`

        :param url: the Instagram URL to send the request to
        """
        return requests.get(
            url,
            headers=self.headers,
            cookies=self.cookies,
            proxies=self.proxies
        )

    def get_user(self, username: str) -> InstaUser:
        """Scrapes an Instagram user's profile and wraps the response

        :param username: the username of the IG user to scrape (without the @)
        :return: an :class:`InstaUser` object, which wraps the response data
        """
        response = self.request(f'https://www.instagram.com/{username}/?__a=1&__d=dis')
        if response.ok:
            try:
                return InstaUser(response.json())
            except JSONDecodeError as e:
                msg = f'Unable to scrape Instagram user @{username} - endpoint potentially deprecated?'
                raise RuntimeError(msg) from e
        else:
            try:
                error = response.json()
            except JSONDecodeError:
                error = response.reason
            raise RuntimeError(
                'Failed to scrape Instagram user @{u}\nResponse: [{code}] -- {e}'.format(
                    u=username, code=response.status_code, e=error
                )
            )

    def download_post(self, post: InstaPost, filepath: str = None) -> bool:
        """Downloads the media from an Instagram post

        :param post: the :class:`~.InstaPost` of the post to download
        :param filepath: the path to save the downloaded media; if ``None``, saves to the :attr:`~DOWNLOAD_DIR`
        """
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
    def headers(self):
        """Headers to use in :meth:`.~request`"""
        return {'User-Agent': self.user_agent, }

    @property
    def cookies(self):
        """Cookies to use in :meth:`.~request`"""
        return {'sessionid': self.session_id, }
