from InstaTweet import InstaTweet
import json

""" 
Let's build a new profile based off a template profile (see create_template.py)
We'll add two users to monitor, as well as hashtags to include when composing tweets 
"""
template_name, profile_name = '', ''
it = InstaTweet.load(template_name)
it.save_profile(profile_name)

"""
The add_users() method accepts users in the form of a single string, an iterable of strings, or an entire user_map
Specify scrape_only=False if you'd like to tweet all of the most recent posts when running the first time (rather than just scraping them).
"""
it.add_users('td_canada')
it.add_users('korn_official', scrape_only=False)

hashtags = ['TDKorn', 'TD', 'Korn']  # General hashtags for all users
for user in it.user_map:
    it.add_hashtags(user, hashtags)

# User-specific hashtags
it.add_hashtags('td_canada', ['finance', 'banking', 'corporate'])
it.add_hashtags('korn_official', ['KornBand', 'metal'])
it.save_profile()
print('User Map:', json.dumps(it.user_map, indent=4), sep='\n')
