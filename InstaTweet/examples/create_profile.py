from InstaTweet import InstaTweet
import json

""" 
    Let's build a profile. If you don't already have a saved profile, please see create_template.py
    Otherwise, you can load your profile like so:
"""

it = InstaTweet.load('Example Template') #autosave=False


"""
    Now we can use the add_users() method to add some users to scrape.
    This method accepts users in the form of a string, Iterable, or full user_map dictionary
    
    You can also specify if you'd like tweets to be sent on the first scrape with the scrape_only parameter. By default,
    scrape_only is set to True, which means that tweets will only be sent for any content posted after the first scrape has been done.     
"""

users = ['badgalriri', 'fentybeauty', 'savagexfenty']
it.add_users(users)


"""
Each user can also have it's own list of hashtags, which will randomly be chosen from each time a tweet is created. 
I'll add some general hashtags to all 3 accounts, as well as some account-specific ones.  
"""

hashtags = ['Rihanna', 'RihannaPleaseStepOnMe', 'Fenty']
for user in it.user_map:
        it.add_hashtags(user, hashtags)

# Add more specific hashtags for Tweets reposted from her brands
it.add_hashtags('fentybeauty', ['makeup', 'FentyBeauty'])
it.add_hashtags('savagexfenty', 'SavageXFenty')

print('User Map: \n', json.dumps(it.user_map, indent=4))


"""Now I'll save the profile so I only have to do this once"""

it.save_profile('Rihanna')


def example_profile():
    """If you'd like this example as a function"""
    users = ['badgalriri', 'fentybeauty', 'savagexfenty']
    hashtags = ['Rihanna', 'RihannaPleaseStepOnMe', 'Fenty']

    print('Loading example template: ')
    it = InstaTweet.load('Example template')

    print('Adding users...')
    it.add_users(users)

    print('Adding hashtags...')
    for user in it.user_map:
        it.add_hashtags(user, hashtags)
    it.add_hashtags('fentybeauty', ['makeup', 'FentyBeauty'])
    it.add_hashtags('savagexfenty', 'SavageXFenty')

    print('User Map: \n', json.dumps(it.user_map, indent=4))
    it.save_profile('Rihanna')
