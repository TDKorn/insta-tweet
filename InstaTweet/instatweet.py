from typing import Optional, List
from . import utils, TweetClient, InstaClient, InstaPost, Profile


class InstaTweet:

    """Uses the settings from a Profile to do the actual InstaTweeting

    You might be wondering, what's InstaTweeting? According to TDK Dictionary:

        **InstaTweet** (`verb`): to scrape an Instagram account -> download & tweet any new content -> update the loaded :class:`~.Profile`

            **Example**

                "Oh, you lost 700 Twitter followers after you shared your IG post? Well maybe if people actually saw the picture
                and not just the caption your tweet would've been less creepy. You should've InstaTweeted it.
        """

    def __init__(self, profile: Profile):
        """Initializes InstaTweet using a fully configured :class:`Profile`

        The :class:`Profile` will be used to initialize an :class:`InstaClient` and :class:`TweetClient`

        :Note:
            Profile settings will only be validated when calling :meth:`~.start`

        :param profile: the profile to use for InstaTweeting
        """
        self.profile = profile
        self.proxies = self.get_proxies()
        self.insta = self.get_insta_client()
        self.twitter = self.get_tweet_client()

    @classmethod
    def load(cls, profile_name: str, local: bool = True) -> "InstaTweet":
        """Loads a profile by name

        :param profile_name: profile name
        :param local: whether the profile is saved locally (True) or remotely on a SQLAlchemy-supported database

        """
        return cls(profile=Profile.load(name=profile_name, local=local))

    def get_proxies(self) -> Optional[dict]:
        """Retrieve proxies using the loaded :class:`Profile` settings"""
        return utils.get_proxies(
            env_key=self.profile.proxy_key
        )

    def get_insta_client(self) -> InstaClient:
        """Initializes an :class:`InstaClient` using the loaded :class:`Profile` settings"""
        return InstaClient(
            session_id=self.profile.session_id,
            user_agent=self.profile.user_agent,
            proxies=self.proxies
        )

    def get_tweet_client(self) -> TweetClient:
        """Initializes an :class:`TweetClient` using the loaded :class:`Profile` settings"""
        return TweetClient(
            profile=self.profile,
            proxies=self.proxies
        )

    def start(self) -> None:
        """InstaTweets all users in the :class:`Profile`'s user map

        Each user will have their profile scraped, and their posts will be compared to their "scraped" list to determine
        if any are new. If there's new posts, the content from them will be downloaded and tweeted

        **Notes**
            * The :class:`Profile` is only saved upon successfully downloading and tweeting a post
                - This allows any failed attempts to be retried in the next call to :meth:`~.start`
            * Error handling/printing is done by :meth:`~.download_post` and :meth:`~.send_tweet`
        """
        profile = self.profile
        profile.validate()

        print(f'Starting InstaTweet for Profile: {profile.name}')

        for user in profile.user_map:
            new_posts = self.get_new_posts(user)
            if not new_posts:
                print(f'No posts to tweet for @{user}')
                continue

            print(f'There are {len(new_posts)} posts to tweet for @{user}')

            for post in new_posts:
                downloaded = self.insta.download_post(post)
                if not downloaded:
                    continue

                tweeted = self.twitter.send_tweet(post, hashtags=profile.get_hashtags_for(user))
                if not tweeted:
                    continue

                profile.get_scraped_from(user).append(post.id)
                profile.get_tweets_for(user).append(post.tweet_data)

                if profile.exists:
                    profile.save(alert=False)

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
        scraped_posts = self.profile.get_scraped_from(username)
        user = self.insta.get_user(username)

        if scraped_posts:
            new_posts = [post for post in user.posts if post.id not in scraped_posts]
            return sorted(new_posts, key=lambda post: post.timestamp)
        else:
            scraped_posts.extend(post.id for post in user.posts)
            print(f'Initialized User: @{username}')
            return None

