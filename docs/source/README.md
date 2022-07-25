# About InstaTweet

## Automatically Repost Content From Instagram to Twitter

Ever tried sharing an Instagram post to Twitter, only to find out that all you tweeted was a link, and not the actual photo/video?<br>

<img src="https://i.imgur.com/4y2gKm2.png" width="75%" height="75%"></img><br>

```{eval-rst}
.. admonition:: ‎ Humiliating 🤮
   :class: important-af

   That could be literally anything. Nobody will click it.

```

<br>

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

```{eval-rst}
.. code::

   #scheduler.py
   from InstaTweet import InstaTweet
   
   PROFILES = ['aProfile', 'myProfile']
   LOCAL = True
    
   def run(profile_name: str, local: bool = LOCAL):
   """Loads and InstaTweets a profile

   :param profile_name: the name of the :class:`~.Profile`
   :param local: if the profile is saved locally or in a SQLAlchemy supported database
   """
   insta_tweet = InstaTweet.load(profile_name, local=local)
   insta_tweet.start()

   if __name__ == '__main__':
      for profile in PROFILES:
         run(profile, local=LOCAL)

```

[//]: # (https://github.com/TDKorn/insta-tweet/blob/1d862bf0c7d04109f5b9e1fe0cb39ac78ed4b114/scheduler.py#L1-L19)

<br>

```{eval-rst}
.. admonition:: But Why? 🤨
   :class: instatweet

   **InstaTweet has two main use cases:** 

   * To automatically share your own Instagram posts to Twitter
   * To automatically tweet new content from other Instagram users

   Regardless of your intention, InstaTweet will detect new posts from the users you specify, download them, and repost
   them to Twitter.
```

<br>

## Documentation

Documentation can be found on [Read the Docs](https://instatweet.readthedocs.io/en/latest/modules.html)

<br>

## Installation

InstaTweet is compatible with Python 3.8 or higher.

To install from [PyPi](https://www.pypi.org/project/insta-tweet) using pip:

```bash
pip install insta-tweet
```

<br>

# Getting Started

**InstaTweet** uses the ```Profile``` class to help manage Twitter accounts, Instagram sessions, and user maps.

```{eval-rst}
.. autoclass:: InstaTweet.profile.Profile
   :show-inheritance:
```

[//]: # (   :members: __init__)

[//]: # (https://github.com/TDKorn/insta-tweet/blob/d08a18a8089c0c2f92c0bf387f7561d0487af0d2/InstaTweet/profile.py#L12-L70)

<br>


You do not need to [```save()```](https://instatweet.readthedocs.io/en/latest/profile.html?highlight=save#InstaTweet.profile.Profile.save) a  profile, but doing so will allow you to easily [```load()```](https://instatweet.readthedocs.io/en/latest/profile.html?highlight=load#InstaTweet.profile.Profile.load) and swap settings

<br>


## Creating a Profile

Settings can be provided as keyword arguments when initializing a ```Profile```, or set directly as object attributes at any point afterwards

* Mandatory settings will have their values validated by [```validate()```](https://instatweet.readthedocs.io/en/latest/profile.html?highlight=validate#InstaTweet.profile.Profile.validate) when calling [```InstaTweet.start()```](https://instatweet.readthedocs.io/en/latest/instatweet_class.html?highlight=start#InstaTweet.instatweet.InstaTweet.start)
* Mandatory settings will have their data **type** validated by property setters at all times
* Requirements are not truly enforced until the profile is *InstaTweeted*


### Mandatory Settings

* ```session_id``` — Instagram Sessionid Cookie, obtained by logging in on a desktop browser
* ```twitter_keys``` — Twitter API Keys with v1.1 endpoint access

### Mandatory Settings with Default Values 

* ```name="default"``` — Profile name; a unique, non-default name is needed to save the ```Profile```, but not to *InstaTweet* it
* ```local=True``` — Indicates if the profile should be saved locally (default) or uploaded to a remote database
* ```user_agent=utils.get_agent()``` — User agent to use when making requests to Instagram/Twitter


### Entirely Optional Settings

- ```proxy_key``` — Environment variable to retrieve proxies from when making requests to Instagram/Twitter
- ```user_map``` — Fully formatted dictionary of IG usernames mapped to their ```USER_MAPPING``` 

***

### Example



```python
from InstaTweet import Profile

# Initialize a profile with arguments
p = Profile(name='myProfile', session_id='session230932041231!!@43rl2204123poopoopee3444')

# Initialize a profile with no arguments
q = Profile()
q.name = 'myProfile'
q.session_id = 'session230932041231!!@43rl2204123poopoopee3444'

p.view_config()
print(f'Same Config: {p.config==q.config}')
```

Output:

```bash
name : myProfile
local : True
session_id : session230932041231!!@43rl2204123poopoopee3444
twitter_keys : {'Consumer Key': 'string', 'Consumer Secret': 'string', 'Access Token': 'string', 'Token Secret': 'string'}
user_agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36
proxy_key : None
user_map : {}
Same Config: True
```

<br>

Note that the profiles don't have their Twitter keys set. This is, for now, a mandatory setting, and so

```python
>>> p.validate()
```
```bash
ValueError: Values not set for the following Twitter keys: ['Consumer Key', 'Consumer Secret', 'Access Token', 'Token Secret']
```

## The User Map

#### The ```user_map``` allows a ```Profile``` to maintain a history of package-related activity for the Instagram users you've added


#### Users are mapped to their ```USER_MAPPING```, which contains their associated lists of:

https://github.com/TDKorn/insta-tweet/blob/74fbbed30376c67eb327297bbb27fc0557c8229e/InstaTweet/profile.py#L27

* ```hashtags``` — the user's associated hashtag list (for use when composing tweets)
* ```scraped``` — the list of posts that have been scraped from the user (only the post id)
* ```tweets``` — the list of sent tweets containing media scraped from that user (limited data)


## Adding Users and Hashtags




***

# STUFF I NEED TO EDIT

## Populating the User Map

The user map is a mapping of Instagram usernames to their associated ```USER_MAPPING```



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

The profile can be saved either locally or to a SQLAlchemy supported database -- just set the ```DATABASE_URL```
environment variable

> **NOTE:** Saving a `Profile` is not mandatory to run InstaTweet, but doing so allows for easy access to associated API 
settings as well as tracking of previously scraped & tweeted posts (which is used to determine which posts are new)    

[//]: # ()
[//]: # (To run InstaTweet, it is mandatory to create and use a ```Profile```. It doesn't need to be saved, but doing)

[//]: # (so will allow you to easily keep track of which posts have been scraped and tweeted already, and, by extension,)

[//]: # (which ones are new. )

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



