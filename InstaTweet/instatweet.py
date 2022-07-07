from typing import Optional, List
from . import utils, TweetClient, InstaClient, InstaPost, Profile


class InstaTweet:

    def __init__(self, profile: Profile):
        """Uses the settings from a Profile to do the actual InstaTweeting

        You might be wondering, what's InstaTweeting? Well, according to TDK Dictionary:

        **InstaTweet** (`verb`):
            To scrape an Instagram user -> download & tweet any new content -> update the Profile's :attr:`~.user_map`
                **Ex.** "Oh, you lost 700 Twitter followers after you shared your IG post? Well maybe your tweet would've
                been less creepy if you InstaTweeted it and people actually saw the picture

        """
        self.profile = profile
        self.proxies = self.get_proxies()
        self.insta = self.get_insta_client()
        self.twitter = self.get_tweet_client()

    @classmethod
    def load(cls, profile_name: str, local: bool = True):
        return cls(profile=Profile.load(name=profile_name, local=local))

    def get_proxies(self):
        return utils.get_proxies(
            env_key=self.profile.proxy_key
        )

    def get_insta_client(self):
        return InstaClient(
            session_id=self.profile.session_id,
            user_agent=self.profile.user_agent,
            proxies=self.proxies
        )

    def get_tweet_client(self):
        return TweetClient(
            profile=self.profile,
            proxies=self.proxies
        )

    def start(self):
        """InstaTweets all users in the :class:`~.Profile`'s user map

        Note that handling and printing of errors is done by :meth:`~.download_post` and :meth:`~.send_tweet`
        """
        self.profile.validate()
        print(f'Starting InstaTweet for Profile: {self.profile.name}')

        for user, user_dict in self.profile.user_map.items():
            new_posts = self.get_new_posts(user)
            if not new_posts:
                print(f'No posts to tweet for @{user}')
                continue

            print(f'There are {len(new_posts)} posts to tweet for @{user}')

            for post in new_posts:
                downloaded = self.insta.download_post(post)
                if not downloaded:
                    continue

                tweeted = self.twitter.send_tweet(post, hashtags=user_dict['hashtags'])
                if not tweeted:
                    continue

                user_dict['scraped'] += [post.id]
                user_dict['tweets'] += [post.tweet_data]

                if self.profile.exists:
                    self.profile.save(alert=False)

            print(f'Finished insta-tweeting for @{user}')

        print(f'All users have been insta-tweeted')

    def get_new_posts(self, username) -> Optional[List[InstaPost]]:
        """Scrapes recent posts from an Instagram user and returns all posts that haven't been tweeted yet

        **NOTE:**  If a user's ``scraped`` list is empty, no posts will be returned.

        Instead, the user is "initialized" as follows:
          * Their ``scraped`` list will be populated with the ID's from the most recent posts
          * These IDs are then used in future calls to the method to determine which posts to tweet

        :param username: the IG username to scrape posts from
        :return: a list of posts that haven't been tweeted yet, or nothing at all (if user is only initialized)

        """
        print(f'Checking posts from @{username}')
        user_dict = self.profile.user_map[username]
        user = self.insta.get_user(username)

        if user_dict['scraped']:
            new_posts = [post for post in user.posts if post.id not in user_dict['scraped']]
            return sorted(new_posts, key=lambda post: post.timestamp)
        else:
            user_dict['scraped'].extend(post.id for post in user.posts)
            print(f'Initialized User: @{username}')
            return None
