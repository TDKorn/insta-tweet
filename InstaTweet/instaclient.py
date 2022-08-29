import os
import requests
from json.decoder import JSONDecodeError
from . import InstaUser, InstaPost


USER_AGENT = "Mozilla/5.0 (Linux; Android 9; GM1903 Build/PKQ1.190110.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36 Instagram 103.1.0.15.119 Android (28/9; 420dpi; 1080x2260; OnePlus; GM1903; OnePlus7; qcom; sv_SE; 164094539)"
"""Hardcoded user agent proven to work with the :meth:`~.InstaClient.get_user` endpoint introduced in v2.0.0b13""

class InstaClient:

    """Minimalistic class for scraping/downloading Instagram user/media data"""

    DOWNLOAD_DIR = os.path.abspath('downloads')  #: [*Optional*] -- Directory to temporarily download media to

    def __init__(self, session_id: str, user_agent: str = USER_AGENT, proxies: dict = None):
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
        self.user_agent = user_agent  # Hardcoded one works for now...
        self.proxies = proxies

        if not os.path.exists(InstaClient.DOWNLOAD_DIR):
            os.mkdir(InstaClient.DOWNLOAD_DIR)

    def request(self, url: str) -> requests.Response:
        """Sends a request using the :attr:`cookies`, :attr:`headers`, and :attr:`proxies`

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
        :return: an :class:`~.InstaUser` object, which wraps the response data
        """
        response = self.request(f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}")
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
    def headers(self) -> dict:
        """Headers to use in :meth:`~.request`"""
        return {'User-Agent': self.user_agent, }

    @property
    def cookies(self) -> dict:
        """Cookies to use in :meth:`~.request`"""
        return {'sessionid': self.session_id, }
