from . import InstaClient, TweetClient, Profile


class InstaTweet:

    def __init__(self, profile: Profile):
        self.profile = profile
        self.scraper = InstaClient(profile.config)
        self.oauth = TweetClient.oauth(profile.twitter_keys)

    @classmethod
    def load(cls, profile_name: str, local: bool = True):
        return cls(profile=Profile.load(name=profile_name, local=local))

    def start(self):
        self.profile.validate()
        for user, user_dict in self.profile.user_map.items():
            new_posts = self.scraper.check_posts(user)
            if not new_posts:
                print(f'No new posts to tweet for @{user}')
                continue

            print(f'There are {len(new_posts)} posts to tweet for @{user}')

            for post in new_posts:
                self.scraper.download_post(post)
                tweet = TweetClient(
                    post=post,
                    auth=self.oauth,
                    hashtags=user_dict['hashtags']
                )
                tweet.send()

                user_dict['scraped'] += [post.id]
                user_dict['tweets'] += [post.tweet]
                if self.profile.exists:
                    self.profile.save(alert=False)

            print(f'Finished insta-tweeting for @{user}')

        print(f'All users have been insta-tweeted')
