# InstaTweet
## Automatically Repost Content From Instagram to Twitter. (The Actual Content)
Ever tried sharing an Instagram post to Twitter, only to find out that all you tweeted was a link, and not the actual photo/video?<br>

<img src="https://i.imgur.com/4y2gKm2.png" width="75%" height="75%"></img><br>

Humiliating. That could be literally anything. Nobody will click it.<br><br>


**InstaTweet shares the *actual* content of the post. Not just a link to it.**<br>

<img src="https://i.imgur.com/C7jc1XS.png" height="50%" width="50%"></img><br>

You can rest easy knowing that, although nobody will click the link, they'll at least see what you posted. Sweet dreams!
<br>
## What's InstaTweet?
InstaTweet is a tool that automates the process of reposting content from Instagram to Twitter. After adding a list of Instagram usernames, InstaTweet will periodically scrape their profiles and check for new posts. If any new content is found, it will be automatically downloaded, cropped, and tweeted. Save InstaTweet profiles to quickly switch between Twitter accounts, Instagram sessions, user lists and hashtag lists.
<br>
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

Regardless of your intention, InstaTweet will detect new posts from the users you specify, download them, and repost them to Twitter.<br>

## Installation
To clone and install this repository with pip:
```bash
python -m pip install git+https://github.com/TDKorn/insta-tweet
```

# Getting Started
InstaTweet uses profiles to help manage Twitter accounts, Instagram sessions, and userlists.

To configure a profile, you'll need to have the following:
* `session_id`  –  Instagram sessionid cookie. You can get one by logging into Instagram on a desktop browser
* `twitter_keys`  –  Twitter API keys with v1.1 access
* `profile_name`  –  Self explanatory
* `user_agent`  –  Optional

As tweets are sent, each profile will update its `user_map` – a mapping of Instagram usernames to their associated:
* Hashtag lists (for use when composing tweets)
* Scraped post history
* Sent tweets history
<br>

Profiles can be saved and reused as templates. Simply load a profile, save it under a new name, and make any changes you'd like. See the [Examples](https://github.com/TDKorn/insta-tweet/blob/master/InstaTweet/examples) folder for more information.
More information can be found in the Examples folder, which also contains profile creation helper functions.<br>

## Creating a Template Profile
Let's create a template profile containing only the `session_id` and `twitter_keys`, as they rarely need to be updated:

```python
from InstaTweet import InstaTweet
import json

session_id = 'sessionid'
twitter_keys = {
    'Consumer Key': 'key',
    'Consumer Secret': 'secret',
    'Access Token': 'token',
    'Token Secret': 'secret'
}

it = InstaTweet(session_id=session_id, twitter_keys=twitter_keys)
it.save_profile('My Template')

print('Profile Settings:\n', json.dumps(it.config, indent=4))
```
Output:
```bash
Using default profile.
Saved profile "My Template"
Profile Settings:
{
    "session_id": "sessionid",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "twitter_keys": {
        "Consumer Key": "key",
        "Consumer Secret": "secret",
        "Access Token": "token",
        "Token Secret": "secret"
    },
    "user_map": {}
}
```

## Using a Template Profile
Now that we've got our template profile saved, we need to add some users to scrape.
For this example, I've created a Twitter account with the username @td_korn, and it'll be a fan account for both TD Bank and the band Korn.
<img src="https://i.imgur.com/Ez4DF0F.png" width="50%" height="25%"></>

<br>
Let's load our template profile and save it under a new name, so that we don't overwrite the template with our changes.

```python
from InstaTweet import InstaTweet

it = InstaTweet.load('My Template')
it.save_profile('tdkorn')
```

Output:
```bash
Loaded profile "My Template"
Saved profile "tdkorn"
```
<br>

### Adding Instagram Users to Monitor
Now that we've got the profile loaded, let's add TD Bank and Korn's Instagram accounts to my user_map

```python
users = ['td_canada', 'korn_official']
it.add_users(users)
```

By default, newly added Instagram users will only have their posts scraped (and not tweeted) the first time InstaTweet runs. Tweets will be sent for any Instagram post uploaded from this point forward.
If you'd prefer to have tweets sent on the first scrape, add your users like so:
```python
it.add_users(users, scrape_only=False)
```
<br>

### Adding Tweet Hashtags
At this point, our user map looks like this:
```bash
{
    "td_canada": {
        "hashtags": [],
        "scraped": [],
        "tweets": []
    },
    "korn_official": {
        "hashtags": [],
        "scraped": [],
        "tweets": []
    }
}
```
<br>

We only need to worry about the `"hashtags"` list. Here, you can specify hashtags to include in tweets when reposting from this user.<br>

Let's add some general hashtags that'll can be included in any tweet, regardless of the account, as well as some account specific ones.
```python
hashtags = ['TDKorn', 'TD', 'Korn']
for user in it.user_map:
        it.add_hashtags(user, hashtags)

it.add_hashtags('td_canada', ['finance', 'banking', 'corporate'])
it.add_hashtags('korn_official', ['KornBand', 'metal'])

print('User Map:', json.dumps(it.user_map, indent=4), sep='\n')
```

Output:
```bash
User Map:
{
    "td_canada": {
        "hashtags": [
            "TDKorn",
            "TD",
            "Korn",
            "finance",
            "banking",
            "corporate"
        ],
        "scraped": [],
        "tweets": []
    },
    "korn_official": {
        "hashtags": [
            "TDKorn",
            "TD",
            "Korn",
            "KornBand",
            "metal"
        ],
        "scraped": [],
        "tweets": []
    }
}
```
<br>

## Running InstaTweet Locally
Once you're satisfied with your profile, all that's left to do is run InstaTweet! You can either run it once:
```python
from InstaTweet import InstaTweet

it = InstaTweet.load('tdkorn')
it.start()
```
Or as a loop that checks for new posts every `delay` seconds:
```python
it.loop(delay=120)
```

## Running InstaTweet on a Server
Coming soon!
