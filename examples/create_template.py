from InstaTweet import InstaTweet
import json

"""
    This example creates a template profile, which can later be loaded, saved under a new name, and further modified. 
    Profile attributes can be set at the time of object initialization or later on via InstaTweet.attribute = value     
"""

session_id = 'string'  # The sessionid cookie is obtained by logging into Instagram from browser
twitter_keys = {       # You must have Twitter API keys with access to Standard v1.1 endpoints
    'Consumer Key': 'string',
    'Consumer Secret': 'string',
    'Access Token': 'string',
    'Token Secret': 'string'
}

it = InstaTweet(session_id=session_id, twitter_keys=twitter_keys)
it.save_profile('My Template')

print('Profile Settings:', json.dumps(it.config, indent=4), sep='\n')


def create_template(template_name, session_id=session_id, twitter_keys=twitter_keys):
    """Function to Create a Template Profile"""
    it = InstaTweet(session_id=session_id, twitter_keys=twitter_keys)
    it.save_profile(template_name)
    print('Profile Settings:', json.dumps(it.config, indent=4), sep='\n')
