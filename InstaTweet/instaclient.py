import requests
from typing import Union
from json.decoder import JSONDecodeError

from . import Profile, InstaUser, InstaPost
from .utils import get_filepath


class InstaClient:

    def __init__(self, profile: Profile):
        if not profile.session_id:
            raise ValueError(f'Profile is missing Instagram sessionid cookie')
        else:
            self.profile = profile

    def request(self, url: str) -> requests.Response:
        return requests.get(url, headers=self.headers, cookies=self.cookies)

    def get_user(self, username: str) -> InstaUser:
        response = self.request(f'https://www.instagram.com/{username}/?__a=1&__d=dis')
        try:
            return InstaUser(response.json())
        # Response status code seems to always be 200, but JSON data is only available if actually successful
        except JSONDecodeError as j:
            raise DeprecationWarning(
                f'Unable to scrape Instagram user @{username}. Endpoint has likely been deprecated') from j
        # In case I'm wrong and there's other reasons for failed requests...
        except Exception as e:
            raise RuntimeError(f'Unable to scrape Instagram user @{username}') from e

    def check_posts(self, username, amount=12) -> Union[list[InstaPost], None]:
        print(f'Checking posts for @{username}')
        scraped_posts = self.profile.user_map[username]['scraped']
        user = self.get_user(username)

        if scraped_posts:
            new_posts = [post for post in user.posts if post.id not in scraped_posts][:amount]
            return sorted(new_posts, key=lambda post: post.timestamp)
        else:
            scraped_posts.extend(post.id for post in user.posts)
            print(f'Initialized User: @{username}')

    def download_post(self, post: InstaPost, filepath=None):
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
        return {
            'User-Agent': self.profile.user_agent
        }

    @property
    def cookies(self):
        return {
            'sessionid': self.profile.session_id
        }
