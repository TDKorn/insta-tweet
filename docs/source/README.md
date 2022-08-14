# InstaTweet - Automatically Repost Content From Instagram to Twitter

Ever tried sharing an Instagram post to Twitter, only to find out that all you tweeted was a link, and not the actual photo/video?<br>

<img src="https://i.imgur.com/4y2gKm2.png" width="75%" height="75%"></img><br>

```{eval-rst}
.. admonition:: ‎ Humiliating 🤮
   :class: important-af

   That could be literally anything. Nobody will click it.

```

**{py:class}`~.InstaTweet` shares the *actual* content of the post. Not just a link to it.**<br>

<img src="https://i.imgur.com/C7jc1XS.png" height="50%" width=auto></img><br>

With `InstaTweet`, you can rest easy knowing that,
although nobody will click the link, they'll at least see what you posted.

<br>

## What's InstaTweet?

`InstaTweet` is a customizable tool to automatically repost content from Instagram to Twitter.

Simply create a {py:class}`~.Profile`, configure the 
{ref}`required settings <mandatory-settings>`, and {py:meth}`~.add_users` to repost from.
Then initialize an {py:class}`~.InstaTweet` object and call {py:meth}`~.start`

```python
from InstaTweet import InstaTweet, Profile

fake_api_keys = {
  'Consumer Key': 'BgHyLeXAtiNpYVeAcEHpBfKCJ',
  'Consumer Secret': 'RCYWdmTGVfkTBFJGZotxQdfUKbKinXMUmZGfKJGmOSCNNKwGMQ',
  'Access Token': '6529716844519798902-JHfRlKwXLgohVpbrtGWQZyNqSDVNEP',
  'Token Secret': 'KShqwycdhKyKyiIbwwzuHQxTYEYAYZgcyIXMolzmpVHJD'
}

# Create and configure a new Profile
p = Profile(
  local=True,
  name='myProfile',
  session_id='6011991A',
  twitter_keys=fake_api_keys
)
p.add_users('the.dailykitten')

# Initialize and run InstaTweet using the Profile directly
insta_tweet = InstaTweet(profile=p)
insta_tweet.start()

# Or save the Profile locally/remotely and load it into InstaTweet by name
p.save()

>>> Saved Local Profile myProfile

insta_tweet = InstaTweet.load('myProfile')
insta_tweet.start()
```

{py:class}`~.InstaTweet` will scrape their profiles and, when new {py:attr}`~.posts` are detected, they'll be 
automatically downloaded and reposted to Twitter.


## Okay... But Why? 😟

[//]: # (The heading above will be hidden via CSS... so it'll look like it links to the admonition below)

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

``InstaTweet`` requires ``Python >= 3.8``

***

To install using pip:

```shell
pip install insta-tweet
```

<br>

# Getting Started

## InstaTweet Profiles

**InstaTweet** uses the {py:class}`~.Profile` class to help manage Twitter accounts, Instagram sessions, and user maps.

```{eval-rst}
.. autodata:: InstaTweet.profile.Profile()
   :annotation:
   :noindex:
```

(settings)=
## Profile Settings
All settings can be configured in two ways: 
1. By passing them as keyword arguments when initializing a {py:class}`~.Profile`  
2. By setting them directly as object attributes after the {py:class}`~.Profile` object is created

<br>

(mandatory-settings)=
### Mandatory Settings

* ```session_id``` — Instagram Sessionid Cookie, obtained by logging in on a desktop browser
* ```twitter_keys``` — Twitter API Keys with v1.1 endpoint access

### Mandatory Settings with Default Values

* ```name="default"``` — profile name; a unique, non-default name is needed to save the {py:class}`~.InstaTweet.Profile`, but not to *InstaTweet* it
* ```local=True``` — Indicates if the profile should be saved locally (default) or on a remote database
* ```user_agent=USER_AGENT``` — User agent to use when making requests to Instagram


### Entirely Optional Settings

- ```proxy_key``` — Environment variable to retrieve proxies from when making requests to Instagram/Twitter
- ```user_map``` — Fully formatted dictionary of IG usernames mapped to their ```USER_MAPPING```

## Creating a New Profile

```python
from InstaTweet import Profile

# Initialize a profile with arguments
p = Profile(
    name='myProfile', 
    session_id='6011991A'
)

# Initialize a profile with no arguments
q = Profile()
q.name = 'myProfile'
q.session_id = '6011991A'
```
All settings can be accessed via the {py:attr}`~.Profile.config` dict. 
If you just want to look, call {py:meth}`~.view_config`

```python
# View and compare configuration settings
q.view_config()
print(f'Same Config: {p.config==q.config}')
```

Output:

```bash
name : myProfile
local : True
session_id : 6011991A
twitter_keys : {'Consumer Key': 'string', 'Consumer Secret': 'string', 'Access Token': 'string', 'Token Secret': 'string'}
user_agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36
proxy_key : None
user_map : {}
Same Config: True
```

<br>

```{eval-rst}
.. admonition:: Validating Profile Settings
   :class: instatweet:

   * Property setters validate data types for the mandatory settings
   * Requirements aren't strictly enforced until :meth:`~.InstaTweet.start` is called, 
     which will first :meth:`~.Profile.validate` the profile settings

```

## Populating the User Map

### The User Map

The {py:attr}`~.user_map` allows a {py:class}`~.Profile` to maintain
a history of package-related activity for its added IG users


Users are mapped to their {py:attr}`~.USER_MAPPING`, which contains their associated lists of:

```python
USER_MAPPING = {'hashtags': [], 'scraped': [], 'tweets': []}
```

* ```hashtags``` — the user's associated hashtag list (for use when composing tweets)
* ```scraped``` — the list of posts that have been scraped from the user (only the post id)
* ```tweets``` — the list of sent tweets containing media scraped from that user (limited data)


The mapping gets updated each time {py:class}`~.InstaTweet` successfully scrapes and tweets a post from the user



<br>

### Adding Users

Use the {py:meth}`~.add_users` method to add one or more Instagram users
to a {py:class}`~.Profile`'s {py:attr}`~.user_map` 

```python
from InstaTweet import Profile

# Add one user at a time
p = Profile('myProfile')
p.add_users('the.dailykitten', send_tweet=True)

>>> Added Instagram user @the.dailykitten to the user map

# Add multiple users at once
usernames = ['dailykittenig','the.daily.kitten.ig']
p.add_users(usernames)

>>> Added Instagram user @dailykittenig to the user map
>>> Added Instagram user @the.daily.kitten.ig to the user map

```

The {py:meth}`~.Profile.get_user` method can be used to retrieve the full {py:attr}`~.USER_MAPPING` of an added user

```python
print(p.get_user('the.dailykitten'))

>>> {'hashtags': [], 'scraped': [-1], 'tweets': []}
```

<br>

### Adding Hashtags

You can {py:meth}`~.add_hashtags` for each user in the {py:attr}`~.user_map`

* They'll be chosen from at random when composing tweets based on one of their {py:attr}`~.posts`
* For more info, see {py:meth}`~.pick_hashtags`, {py:meth}`~.build_tweet` and {py:meth}`~.send_tweet` 

```python
# Add a single hashtag for a specific user
p.add_hashtags(user='dailykittenig', hashtags='cats')

>>> Added hashtags for @dailykittenig

# Add multiple hashtags at once
users = ['the.dailykitten','the.daily.kitten.ig']
hashtags = ['kittygram', 'kittycat']

for user in users:
    p.add_hashtags(user, hashtags)

>>> Added hashtags for @the.dailykitten
>>> Added hashtags for @the.daily.kitten.ig

p.view_config()
```
Output:
```shell
name : myProfile
local : True
session_id : 6011991A
twitter_keys : {'Consumer Key': 'string', 'Consumer Secret': 'string', 'Access Token': 'string', 'Token Secret': 'string'}
user_agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36
proxy_key : None
user_map : {'the.dailykitten': {'hashtags': ['kittygram', 'kittycat'], 'scraped': [-1], 'tweets': []}, 'dailykittenig': {'hashtags': ['cats'], 'scraped': [], 'tweets': []}, 'the.daily.kitten.ig': {'hashtags': ['kittygram', 'kittycat'], 'scraped': [], 'tweets': []}}
```

You can use the {py:meth}`~.get_hashtags_for` method to retrieve the `hashtags` list of a specific username

```python
print(p.get_hashtags_for('the.daily.kitten.ig'))

>>> ['kittygram', 'kittycat']
```

<br>

### Methods Related to User Map Access

```{eval-rst}
.. admonition:: User Map Access Methods
    :class: instatweet

    The `Profile` has several methods that allow for easy access to the {py:attr}`~.user_map`

    * :meth:`~.Profile.get_user` provides access to a particular user's {py:attr}`~.USER_MAPPING`
    * :meth:`~.get_scraped_from` returns the list of posts scraped from a specified user  
    * :meth:`~.get_hashtags_for` returns the list of hashtags to use in tweets for the specified user
    * :meth:`~.get_tweets_for` returns a list of tweets that use the specified user's scraped content

    All lists returned by the :attr:`~.user_map` access methods can be modified in place. For example:

    .. code::
    
      p.get_hashtags_for('the.daily.kitten.ig').append('kittypoop')
      print(p.get_hashtags_for('the.daily.kitten.ig'))
      
      >>> ['kittygram', 'kittycat', 'kittypoop']
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

Call {py:meth}`~.save` on a {py:class}`~.Profile` to save it using the current or specified {py:attr}`~.name`

The value of {py:attr}`~.local` determines the location and save format:

* If ```local=True```, the profile will be saved as a pickle file in the ```Profile.LOCAL_DIR```

* Otherwise, the profile will be saved to the database specified by the ```DATABASE_URL``` environment variable
  - The {py:class}`~.Profiles` database table stores the {py:class}`~.Profile` as pickle bytes (via {py:meth}`~.to_pickle`)


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



## Schedule InstaTweet

You can easily schedule InstaTweet using the provided [scheduler](https://github.com/tdkorn/insta-tweet/blob/2.0.0/scheduler.py) 
script

```{literalinclude} ../../scheduler.py
```

FROM COMMIT d287295


