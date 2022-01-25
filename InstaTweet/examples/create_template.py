from InstaTweet import InstaTweet
import json

"""
    This example creates a template profile, which can later be loaded, modified, and saved as a new profile. 
    The template profile contains the Instagram sessionid cookie and Twitter API keys as they rarely need to be updated.
    Profile attributes can be set at the time of object initialization or later on via InstaTweet.attribute = value     
"""
# Sessionid cookie is obtained by logging into Instagram from browser
session_id = 'string'

# You must have a Twitter developer account with access to Standard v1.1 endpoints
twitter_keys = {
    'Consumer Key': 'string',
    'Consumer Secret': 'string',
    'Access Token': 'string',
    'Token Secret': 'string'
}

it = InstaTweet(session_id=session_id, twitter_keys=twitter_keys)
it.save_profile('Example Template')

print('Profile Settings:', json.dumps(it.config, indent=4), sep='\n')


def example_template():
    """If you'd like this example as a function"""
    it = InstaTweet(session_id=session_id, twitter_keys=twitter_keys)
    it.save_profile('Example Template')
    print('Profile Settings:', json.dumps(it.config, indent=4), sep='\n')
