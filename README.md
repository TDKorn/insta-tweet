# InstaTweet
## Automatically Repost Content From Instagram to Twitter
Ever tried sharing an Instagram post to Twitter, only to find out that all you tweeted was a link, and not the actual photo/video?<br>

<img src="https://i.imgur.com/4y2gKm2.png" width="75%" height="75%"></img><br>

Humiliating. That could be literally anything. Nobody will click it.<br><br>


**InstaTweet shares the *actual* content of the post. Not just a link to it.**<br>

<img src="https://i.imgur.com/C7jc1XS.png" height="50%" width="50%"></img><br>

With InstaTweet, you can rest easy knowing that, although nobody will click the link, they'll at least see what you posted.

<br>

## What's InstaTweet?
InstaTweet is a tool that automatically reposts content from Instagram to Twitter. 

Simply create a ```Profile```, configure the necessary settings, and add the Instagram users you'd like repost from. 
InstaTweet will then periodically scrape their accounts and, if new posts are detected, they'll be automatically
downloaded and posted to Twitter.

<br>

Once you've got a ```Profile``` set up, using InstaTweet is as simple as:

```python
from InstaTweet import InstaTweet

insta_tweet = InstaTweet.load('myProfile')
insta_tweet.start()
```

<br>

The [scheduler](scheduler.py) can also be used (remotely and locally) to InstaTweet your profile(s)

https://github.com/TDKorn/insta-tweet/blob/1d862bf0c7d04109f5b9e1fe0cb39ac78ed4b114/scheduler.py#L1-L19

<br>

## Why?

InstaTweet has two main use cases:
1. To automatically share your own Instagram posts to Twitter
2. To automatically tweet new content from other Instagram users

Regardless of your intention, InstaTweet will detect new posts from the users you specify, download them, and repost
them to Twitter.

<br>

## Documentation

Documentation can be found on [Read the Docs](https://instatweet.readthedocs.io)

<br>

## Installation

Install InstaTweet using pip:

```bash
pip install insta-tweet
```

<br>

# Getting Started

InstaTweet uses the ```Profile``` class to help manage Twitter accounts, Instagram sessions, and user maps

https://github.com/TDKorn/insta-tweet/blob/dc904af214596588bfc75b32eccc1ff37d0c271b/InstaTweet/profile.py#L12-L49

<br>

To run InstaTweet, it is mandatory to create and use a ```Profile```. It doesn't need to be saved, but doing
so will allow you to easily keep track of which posts have been scraped and tweeted already, and, by extension,
which ones are new. 

A ```Profile``` can be saved locally or to a SQLAlchemy supported database --  just set the ```DATABASE_URL``` 
environment variable

<br>

## Profile Settings

To fully configure a ```Profile``` for InstaTweeting, you'll need to set the following attributes:
* `session_id`  –  Instagram sessionid cookie. You can get one by logging into Instagram on a desktop browser
* `twitter_keys`  –  Twitter API keys with v1.1 access


<br>

Optionally, you can also set the following:
* `local`  –  Indicates if the profile should be saved locally (default) or on a SQLAlchemy supported database
* `proxy_key`  –  Environment variable to retrieve proxies from when making requests to Instagram/Twitter
* `user_agent`  – User agent to use when making requests to Instagram/Twitter
* `name`  –  used for saving; must be unique

<br>

As tweets are sent, each profile will update its `user_map` – a mapping of Instagram usernames to their associated lists of:
* ```hashtags``` -- the user's associated hashtag list (for use when composing tweets)
* ```scraped``` -- the list of posts that have been scraped from the user (only the post id)
* ```tweets``` -- the list of sent tweets containing media scraped from that user (limited data)

<br>

## Creating a Profile

When creating a ```Profile```, you can specify arguments at the time of object initialization, or at any point afterwards. 

```python
from InstaTweet import Profile

# Initialize a Profile with no arguments
p = Profile()

# Initialize a Profile with arguments
q = Profile('myProfile', local=False, session_id='SNKIASFD93WI4R920DWQ')

# Set Profile attributes after initialization
r = Profile()
r.name = 'aProfile'
r.proxy_key = 'QUOTAGUARD_STATIC'


print('Profile 1')
p.view_config()

print('\nProfile 2')
q.view_config()

print('\nProfile 3')
r.view_config()

```
Output:
```shell
Profile 1
name : default
local : True
session_id : 
twitter_keys : {'Consumer Key': 'string', 'Consumer Secret': 'string', 'Access Token': 'string', 'Token Secret': 'string'}
user_agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36
proxy_key : None
user_map : {}

Profile 2
name : myProfile
local : False
session_id : SNKIASFD93WI4R920DWQ
twitter_keys : {'Consumer Key': 'string', 'Consumer Secret': 'string', 'Access Token': 'string', 'Token Secret': 'string'}
user_agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36
proxy_key : None
user_map : {}

Profile 3
name : aProfile
local : True
session_id : 
twitter_keys : {'Consumer Key': 'string', 'Consumer Secret': 'string', 'Access Token': 'string', 'Token Secret': 'string'}
user_agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36
proxy_key : QUOTAGUARD_STATIC
user_map : {}
```

<br>

## Populating the User Map

The user map is a mapping of Instagram usernames to their associated ```USER_MAPPING```

https://github.com/TDKorn/insta-tweet/blob/dc904af214596588bfc75b32eccc1ff37d0c271b/InstaTweet/profile.py#L14

<br>

The mapping gets updated as InstaTweet runs, when posts are successfully scraped and tweeted from these users.
The ```Profile``` has methods to easily access and modify these mappings

### Adding Users

Use the ```add_users()``` method to add users to a Profile's user map

```python
from InstaTweet import Profile

>>> p = Profile('myProfile')
>>> p.add_users('username')

Added Instagram user @username to the user map

>>> usernames = ['user','names']
>>> p.add_users(usernames)

Added Instagram user @user to the user map
Added Instagram user @names to the user map

>>> p.view_config()
```
```shell
name : myProfile
local : True
session_id : 
twitter_keys : {'Consumer Key': 'string', 'Consumer Secret': 'string', 'Access Token': 'string', 'Token Secret': 'string'}
user_agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36
proxy_key : None
user_map : {'username': {'hashtags': [], 'scraped': [], 'tweets': []}, 'user': {'hashtags': [], 'scraped': [], 'tweets': []}, 'names': {'hashtags': [], 'scraped': [], 'tweets': []}}
```

You can use the ```get_user()``` method to retrieve the mapping of a particular user
```python
>>> print(p.get_user('names'))

{'hashtags': [], 'scraped': [], 'tweets': []}
```
***

### Adding Hashtags
Use the ```add_hashtags()``` method to add hashtags to a specific user in the Profile's user map

```python
>>> p.add_hashtags(user='username', hashtags='cool')

Added hashtags for @username

>>> hashtags = ['wow', 'okay']
>>> p.add_hashtags('user', hashtags)

Added hashtags for @user

>>> print(p.user_map)
{'username': {'hashtags': ['cool'], 'scraped': [], 'tweets': []}, 'user': {'hashtags': ['wow', 'okay'], 'scraped': [], 'tweets': []}, 'names': {'hashtags': [], 'scraped': [], 'tweets': []}}
```

You can use the ```get_hashtags_for()``` method to retrieve the hashtag list of a specific username

```python
>>> print(p.get_hashtags_for('user'))

['wow', 'okay']
```

<br> 

## Saving a Profile

Call ```save()``` to save the profile using the current or specified profile ```name```. The value of ```local``` determines the location and save format

* If ```local=True```, the profile will be saved as a pickle file in the ```Profile.LOCAL_DIR```

* Otherwise, the profile will be saved to the database specified by the ```DATABASE_URL``` environment variable
  - It gets converted to a pickle byte string (via ```to_pickle()```), which is then used to add/update a row

<br>

https://github.com/TDKorn/insta-tweet/blob/dc904af214596588bfc75b32eccc1ff37d0c271b/InstaTweet/profile.py#L142-L147

<br>

#### Example: 
```python
>>> p = Profile('myProfile')
>>> p.save()

Saved Local Profile myProfile
```

<br>

Note that you can specify a new name for the profile at the time of saving, but it still must be unique

```python
>>> q = Profile()
>>> q.save('aProfile')

Saved Local Profile aProfile

>>> q.save('myProfile')

FileExistsError: Local save file already exists for profile named "myProfile"
Please choose another name, load the profile, or delete the file.
```

<br>

You can see if a profile name already exists remotely or locally by calling the ```profile_exists()``` static method:

https://github.com/TDKorn/insta-tweet/blob/dc904af214596588bfc75b32eccc1ff37d0c271b/InstaTweet/profile.py#L79-L86

<br>

