import requests
from . import InstaPost, InstaUser


class InstaClient(object):
    """Instagram client to scrape and download posts"""

    def __init__(self, profile: dict):
        self.profile = profile
        self.user_map = profile['user_map']
        self.headers = {
            'User-Agent': profile['user_agent']
        }
        self.cookies = {
            'sessionid': profile['session_id']
        }

    def request(self, url):
        return requests.get(url, headers=self.headers, cookies=self.cookies)

    def check_posts(self, username, amount=12):
        print('Checking posts for @' + username)
        user = self.get_user(username)
        scraped_posts = self.user_map[username]['scraped']

        if scraped_posts:
            return [post for post in user.posts if post.id not in scraped_posts][:amount]
        else:
            # By default, this would be a newly added user
            scraped_posts.extend([post.id for post in user.posts])
            print(f'Initialized User: @{username}')

    def get_user(self, username):
        response = self.request(f'https://www.instagram.com/{username}/?__a=1')
        if not response.ok:
            raise Exception(response.json())
        else:
            return InstaUser(response.json())

    def download_post(self, post: InstaPost, filepath):
        response = self.request(post.media_url)
        if response.ok:
            filepath = filepath.split('.')[0] + '.mp4' if post.is_video else '.png'
            with open(filepath, 'wb') as f:
                f.write(response.content)
            post.file_path = filepath
            print(f'Downloaded post {post.id} by {post.owner["username"]} from {post.permalink}')
        else:
            raise RuntimeError(f'Failed to download post {post.permalink} by {post.owner["username"]}')
