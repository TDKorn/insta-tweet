from typing import Optional, List, Dict
from . import utils, TweetClient, InstaClient, InstaPost, Profile


class InstaTweet:

    """Uses the settings from a Profile to do the actual InstaTweeting

    You might be wondering, what's InstaTweeting? According to TDK Dictionary:

        .. admonition:: **InstaTweet** (`verb`):
           :class: instatweet

           To load a :class:`~.Profile` 🠖 scrape :attr:`~.posts` from its Instagram pages
           🠖 :meth:`~.download_post` & :meth:`~.send_tweet` for any new content
           🠖 update the :attr:`~.page_map`
           🠖 :meth:`~.save` the profile if it :attr:`~.exists`

            .. admonition:: **Example Sentence**
               :class: example

               Oh, you lost 700 Twitter followers after you shared your IG post? Well maybe if people actually saw the
               picture and not just the caption your tweet would've been less creepy. You should've InstaTweeted it.

    """

    def __init__(self, profile: Profile):
        """Initializes :class:`~.InstaTweet` using a fully configured :class:`~.Profile`

        The :class:`~.Profile` will be used to initialize an :class:`~.InstaClient` and :class:`~.TweetClient`

        .. note:: InstaTweet won't :meth:`~.validate` the Profile settings until you call :meth:`~.start`

        :param profile: the :class:`~.Profile` to use for InstaTweeting
        """
        self.profile = profile
        self.proxies = self.get_proxies()
        self.insta = self.get_insta_client()
        self.twitter = self.get_tweet_client()

    @classmethod
    def load(cls, profile_name: str, local: bool = True) -> "InstaTweet":
        """Loads a profile by name

        :param profile_name: name of the Profile to load
        :param local: whether the profile is saved locally (default) or remotely on a database
        """
        return cls(profile=Profile.load(name=profile_name, local=local))

    def get_proxies(self) -> Optional[Dict]:
        """Retrieve proxies using the loaded Profile's :attr:`~Profile.proxy_key`"""
        return utils.get_proxies(
            env_key=self.profile.proxy_key
        )

    def get_insta_client(self) -> InstaClient:
        """Initializes an :class:`~.InstaClient` using the loaded :class:`~.Profile` settings"""
        return InstaClient(
            session_id=self.profile.session_id,
            user_agent=self.profile.user_agent,
            proxies=self.proxies
        )

    def get_tweet_client(self) -> TweetClient:
        """Initializes an :class:`~.TweetClient` using the loaded :class:`~.Profile` settings"""
        return TweetClient(
            profile=self.profile,
            proxies=self.proxies
        )

    def start(self, max_posts: int = 12) -> None:
        """InstaTweets all pages that have been added to the loaded :class:`~.Profile`

        The most recent posts from each page will be scraped, then compared to the ``scraped``
        list in the :attr:`~.PAGE_MAPPING` to determine which are new.

        Up to ``max_posts`` new posts from each page will then be downloaded and tweeted

        .. note:: If ``InstaTweet`` fails to :meth:`~.download_post` or :meth:`~.send_tweet`,
           the :attr:`~.PAGE_MAPPING` won't be updated

           * This ensures that failed repost attempts are retried in the next call to :meth:`~start`

           If a save file for the Profile already :attr:`~.exists`, successful reposts
           will trigger a call to :meth:`~.save`

        :param max_posts: the maximum number of new posts to download and tweet per page
        """
        profile = self.profile
        profile.validate()

        print(f'Starting InstaTweet for Profile: {profile.name}')

        for page in profile.page_map:
            page_name = page if page.startswith("#") else "@" + page

            if not (new_posts := self.get_new_posts(page)):
                print(f'No posts to tweet for {page_name}')
                continue

            print(f'There are {len(new_posts)} posts to tweet for {page_name}')
            hashtags = profile.get_hashtags_for(page)

            for post in new_posts[:max_posts]:
                self.insta.download_post(post)
                if not post.is_downloaded:
                    continue

                tweeted = self.twitter.send_tweet(post, hashtags)
                if not tweeted:
                    continue

                profile.get_scraped_from(page).append(post.id)
                profile.get_tweets_for(page).append(post.tweet_data)

                if profile.exists:
                    profile.save(alert=False)

            print(f'Finished insta-tweeting for {page_name}')

        print(f'All pages have been insta-tweeted')

    def get_new_posts(self, insta_page: str) -> Optional[List[InstaPost]]:
        """Scrapes recent posts from an Instagram page and returns all posts that haven't been tweeted yet

        **NOTE:**  If a page's ``scraped`` list is empty, no posts will be returned.

        Instead, the page is "initialized" as follows:

        * The ``scraped`` list will be populated with the ID's from the most recent posts
        * These IDs are then used in future method calls to determine which posts to tweet

        :param insta_page: the Instagram page to scrape posts from
        :return: a list of posts that haven't been tweeted yet, or nothing at all (if page is only initialized)

        """
        print(f'Checking posts from {insta_page}')
        scraped_posts = self.profile.get_scraped_from(insta_page)
        page = self.insta.scrape(insta_page)

        if scraped_posts:
            new_posts = [post for post in page.posts if post.id not in scraped_posts]
            return sorted(new_posts, key=lambda post: post.timestamp)
        else:
            scraped_posts.extend(post.id for post in page.posts)
            print(f'Initialized {page}')
            return None

