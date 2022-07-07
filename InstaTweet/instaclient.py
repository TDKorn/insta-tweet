import requests

from .utils import get_filepath, get_agent
from json.decoder import JSONDecodeError
from . import InstaUser, InstaPost


class InstaClient:

    def __init__(self, session_id: str, user_agent: str = None):
        """Minimalistic class for scraping/downloading Instagram user/media data

        :param session_id: valid Instagram sessionid cookie from a browser
        :param user_agent: user agent to use in requests made by the class
        """
        if not isinstance(session_id, str):
            raise TypeError('session_id must be a string')

        self.session_id = session_id
        self.user_agent = user_agent if user_agent else get_agent()

    def request(self, url: str) -> requests.Response:
        """Sends a request using the sessionid cookie and user agent

        :param url: the URL to send the request to; should be an Instagram link, but not necessary
        """
        return requests.get(url, headers=self.headers, cookies=self.cookies)

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
                    u=username, code=response.status_code, e=error)
            )

    def download_post(self, post: InstaPost, filepath: str = None) -> bool:
        """Downloads the media from an Instagram post

        :param post: the :class:`~.InstaPost` of the post to download
        :param filepath: the location to save the downloaded file (optional)
        """
        response = self.request(post.media_url)
        if not response.ok:
            raise RuntimeError(
                f'Failed to download post {post.permalink} by {post.owner["username"]}'
            )
        if filepath is None:
            filepath = get_filepath(
                filename=post.id,
                filetype='mp4' if post.is_video else 'jpg'
            )
        with open(filepath, 'wb') as f:
            f.write(response.content)
            post.filepath = filepath

        print(f'Downloaded post {post.permalink} by {post.owner["username"]} to {post.filepath}')
        return True

    @property
    def headers(self):
        """Headers to use in :meth:`.~request`"""
        return {'User-Agent': self.user_agent, }

    @property
    def cookies(self):
        """Cookies to use in :meth:`.~request`"""
        return {'sessionid': self.session_id, }
