import requests
from . import InstaPost, InstaUser
from .utils import get_filepath


class InstaClient(object):
    """
    Instagram client to scrape and download posts
    """

    def __init__(self, profile: dict):
        self.session_id = profile['session_id']
        self.user_map = profile['user_map']
        self.user_agent = profile['user_agent']

    def request(self, url):
        return requests.get(url, headers=self.headers, cookies=self.cookies)

    def check_posts(self, username, amount=12):
        print('Checking posts for @' + username)
        user = self.get_user(username)
        scraped_posts = self.user_map[username]['scraped']

        if scraped_posts:
            # Return a list of {amount} InstaPost objects, sorted from oldest to newest (oldest is tweeted first).
            posts = [post for post in user.posts if post.id not in scraped_posts][:amount]
            return sorted(posts, key=lambda p: p.timestamp)
        else:
            # By default, newly added users have an empty scraped post list and are only initialized on the first run.
            scraped_posts.extend([post.id for post in user.posts])
            print(f'Initialized User: @{username}')
            return None     # No posts to tweet

    def get_user(self, username):
        response = self.request(f'https://www.instagram.com/{username}/?__a=1')
        if not response.ok:
            raise Exception(response.json())
        else:
            return InstaUser(response.json())

    def download_post(self, post: InstaPost, filepath=None):
        response = self.request(post.media_url)
        if not response.ok:
            raise RuntimeError(f'Failed to download post {post.permalink} by {post.owner["username"]}')

        if filepath is None:
            filetype = 'mp4' if post.is_video else 'jpg'
            filepath = get_filepath(post.id, filetype=filetype)
        with open(filepath, 'wb') as f:
            f.write(response.content)

        post.file_path = filepath
        print(f'Downloaded post {post.id} by {post.owner["username"]} from {post.permalink}')

    # Properties so that changes to sessionid/useragent will be reflected
    @property
    def cookies(self):
        return {
            'sessionid': self.session_id
        }

    # TODO See if any other cookies/headers should be included
    @property
    def headers(self):
        return {
            'User-Agent': self.user_agent
        }

    @property
    def session_id(self):
        return self._session_id

    @session_id.setter
    def session_id(self, session_id: str):
        if not isinstance(session_id, str):
            raise ValueError('Session ID cookie must be of type str')
        self._session_id = session_id
