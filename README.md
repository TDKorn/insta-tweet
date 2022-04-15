# InstaTweet
A customizable tool to automatically repost content from Instagram to Twitter. The actual content.

## What's InstaTweet?

InstaTweet is a tool that automates the process of reposting content from Instagram to Twitter. After adding a list of Instagram usernames, InstaTweet will periodically scrape their profiles and check for new posts. If any new content is found, it will be automatically downloaded, cropped, and tweeted. Save InstaTweet profiles to quickly switch between Twitter accounts, Instagram sessions, user lists and hashtag lists.

Once you've configured a profile, using InstaTweet is as simple as:

```python
from InstaTweet import InstaTweet

it = InstaTweet.load('My Profile')
it.start()
```

You can also run it as a loop for a single profile:

```python
it.loop(delay=120)
```
Or you can loop through multiple profiles:
```python
profiles = ['profile1', 'profile2', 'profile3']

for profile in profiles:
    it = InstaTweet.load(profile)
    it.start()
```

## Why?
InstaTweet has two main use cases:
1. To automatically share your own Instagram posts to Twitter 
2. To automatically tweet new content from other Instagram users 

Regardless of your intention, InstaTweet will detect new posts from the users you specify and repost them to Twitter.  <br><br>

You might be wondering: what's the point? Why not just share from the Instagram app like a normal person?  <br>

<b><ins>Because all that does is tweet a link. It's humiliating. Literally nobody will click it.</b>
<br>

![](https://i.imgur.com/4y2gKm2.png)  <br>

### <b><ins>InstaTweet shares the actual media. Not just a link.</b> 

![](https://i.imgur.com/C7jc1XS.png)  <br>
    
With InstaTweet, you can rest easy knowing that, although nobody will click the link, they'll at least see what you posted. Sweet dreams!

<br>
    
## Installation
To clone and install this repository with pip:
```bash
python -m pip install git+https://github.com/TDKorn/insta-tweet
```
<br>

# Getting Started
InstaTweet uses profiles to help manage Twitter accounts, Instagram sessions, and userlists.

Each profile has its own:
* Instagram sessionid cookie 
* Twitter API keys
* User Agent 
* User Map
* Name
 
<br>

The User Map is a mapping of Instagram usernames to their associated:
* Hashtag lists (for use when composing tweets)
* Scraped post history
* Sent tweets history

<br>

Profiles can be saved and reused as templates - simply load a profile, make modifications, and save it under a new name.

More information can be found in the examples folder, which also contains profile creation helper functions.

<br>

## Creating a Template Profile
To get started, you'll need 
* An Instagram sessionid cookie, which can be obtained by logging into Instagram on a desktop browser
* The Twitter API keys from a developer account that has access to Standard v1.1 endpoints

<br>

Let's create a template profile containing only these attributes, as they rarely need to be updated:

```python
from InstaTweet import InstaTweet
import json

session_id = 'string'
twitter_keys = {
    'Consumer Key': 'string',
    'Consumer Secret': 'string',
    'Access Token': 'string',
    'Token Secret': 'string'
}

it = InstaTweet(session_id=session_id, twitter_keys=twitter_keys)
it.save_profile('My Template')

print('Profile Settings:', json.dumps(it.config, indent=4), sep='\n')
```
Output:
```bash
Saved profile "My Template"
Profile Settings:
{
    "session_id": "string",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "twitter_keys": {
        "Consumer Key": "string",
        "Consumer Secret": "string",
        "Access Token": "string",
        "Token Secret": "string"
    },
    "user_map": {}
}
```
<br>

## Using a Template Profile
Now that we've got our template profile saved, we need to add some users to scrape. For this example, I've created a Twitter fan account for Rihanna with the username `@RihannasWetSock`, which will help demonstrate the setup process.


### Adding Users
Let's load our template profile and add Rihanna's Instagram account and her brand accounts to it.
```python
from InstaTweet import InstaTweet

it = InstaTweet.load('My Template')
users = ['badgalriri', 'fentybeauty', 'savagexfenty']
it.add_users(users)
```

By default, newly added users will only have their posts scraped the first time InstaTweet runs. Tweets will be sent for any Instagram post uploaded from this point forward.
If you'd prefer to have tweets sent on the first scrape, add your users like so:
```python
it.add_users(users, scrape_only=False)
```

### Adding Tweet Hashtags
Each user can also have it's own list of hashtags, which will randomly be chosen from each time a tweet is created. Let's add some general hashtags to all 3 accounts, as well as some more specific ones for her brands. I'll then save the profile so that I only have to do this once.

```python
hashtags = ['Rihanna', 'RihannaPleaseStepOnMe', 'Fenty']
for user in it.user_map:
        it.add_hashtags(user, hashtags)

# Add more specific hashtags for Tweets reposted from her brands
it.add_hashtags('fentybeauty', ['makeup', 'FentyBeauty'])
it.add_hashtags('savagexfenty', 'SavageXFenty')

print('User Map: \n', json.dumps(it.user_map, indent=4))
it.save_profile('Rihanna')
```

Output:
```bash
Loaded profile "My Template"
User Map:
  {
    "badgalriri": {
        "hashtags": [
            "Rihanna",
            "RihannaPleaseStepOnMe",
            "Fenty"
        ],
        "scraped": [],
        "tweets": []
    },
    "fentybeauty": {
        "hashtags": [
            "Rihanna",
            "RihannaPleaseStepOnMe",
            "Fenty",
            "makeup",
            "FentyBeauty"
        ],
        "scraped": [],
        "tweets": []
    },
    "savagexfenty": {
        "hashtags": [
            "Rihanna",
            "RihannaPleaseStepOnMe",
            "Fenty",
            "SavageXFenty"
        ],
        "scraped": [],
        "tweets": []
    }
}
Saved profile "Rihanna"
```
<br>

## Running InstaTweet
Once you're satisfied with your profile, all that's left to do is run InstaTweet! You can either run it once:
```python
from InstaTweet import InstaTweet

it = InstaTweet.load('Rihanna')
it.start()
```
Or as a loop that checks for new posts every `delay` seconds:
```python
it.loop(delay=120)
```
