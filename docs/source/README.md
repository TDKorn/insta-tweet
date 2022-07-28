# InstaTweet v2.0.0b13

## Automatically Repost Content From Instagram to Twitter

Ever tried sharing an Instagram post to Twitter, only to find out that all you tweeted was a link, and not the actual photo/video?<br>

<img src="https://i.imgur.com/4y2gKm2.png" width="75%" height="75%"></img><br>

[//]: # (![image]&#40;https://user-images.githubusercontent.com/96394652/180762012-736d6296-bb13-4b47-afb6-53b5c4a9a408.png&#41;)




```{eval-rst}
.. admonition:: ‎ Humiliating 🤮
   :class: important-af

   That could be literally anything. Nobody will click it.

```

[//]: # (```{eval-rst}  )

[//]: # (`Load <profile.html#InstaTweet.profile.Profile.load>`_)

[//]: # (```)

[//]: # ({py:meth}`~InstaTweet.profile.Profile.load`)

[//]: # (```)


<br>

**{py:class}`~.InstaTweet` shares the *actual* content of the post. Not just a link to it.**<br>

<img src="https://i.imgur.com/C7jc1XS.png"></img><br>

[//]: # (height="50%" width="50%"></img><br>)

[//]: # (![image]&#40;https://user-images.githubusercontent.com/96394652/180762389-3b697c8d-d9ba-48bb-9646-7d7ab1912cb0.png&#41;)

With InstaTweet, you can rest easy knowing that, although nobody will click the link, they'll at least see what you posted.

<br>

## What's InstaTweet?

`InstaTweet` is a tool that automatically reposts content from Instagram to Twitter.

Simply create a {py:class}`~.InstaTweet.Profile`, configure the 
{ref}`required settings <mandatory-settings>`, and {py:meth}`~.add_users` to repost from.
Once you {py:meth}`~.validate` the profile, you can {py:meth}`~.InstaTweet.load` it 
into an {py:class}`~.InstaTweet` object and call {py:meth}`~.start`

```python
from InstaTweet import InstaTweet

insta_tweet = InstaTweet.load('myProfile')
insta_tweet.start()
```

`InstaTweet` will then scrape the users you added and when new posts are detected, they'll be automatically
downloaded and reposted to Twitter.

You can also use the provided [scheduler.py](https://github.com/tdkorn/insta-tweet/blob/2.0.0/scheduler.py) 
file to InstaTweet your local/remote profiles:

```{literalinclude} ../../scheduler.py
```

<br>

[//]: # (https://github.com/TDKorn/insta-tweet/blob/1d862bf0c7d04109f5b9e1fe0cb39ac78ed4b114/scheduler.py#L1-L19)


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

InstaTweet requires ``Python 3.8`` or higher

To install using pip:

```bash
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

[//]: # (https://github.com/TDKorn/insta-tweet/blob/d08a18a8089c0c2f92c0bf387f7561d0487af0d2/InstaTweet/profile.py#L12-L70)


(settings)=
## Creating a Profile

All settings can be passed as arguments when initializing a {py:class}`~.InstaTweet.Profile`, 
or set directly as object attributes at any point afterwards

* Property setters validate data types for the mandatory settings
* Requirements aren't strictly enforced until {py:meth}`.InstaTweet.start` is called,
  at which point the profile as a whole is validated by {py:meth}`~.validate`


(mandatory-settings)=
### Mandatory Settings

* ```session_id``` — Instagram Sessionid Cookie, obtained by logging in on a desktop browser
* ```twitter_keys``` — Twitter API Keys with v1.1 endpoint access

### Mandatory Settings with Default Values

* ```name="default"``` — Profile name; a unique, non-default name is needed to save the {py:class}`~.InstaTweet.Profile`, but not to *InstaTweet* it
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
p = Profile(
    name='myProfile', 
    session_id='US6011991A'
)

# Initialize a profile with no arguments
q = Profile()
q.name = 'myProfile'
q.session_id = 'US6011991A'

# View and compare configuration settings
q.view_config()
print(f'Same Config: {p.config==q.config}')
```

Output:

```bash
name : myProfile
local : True
session_id : US6011991A
twitter_keys : {'Consumer Key': 'string', 'Consumer Secret': 'string', 'Access Token': 'string', 'Token Secret': 'string'}
user_agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36
proxy_key : None
user_map : {}
Same Config: True
```

[//]: # (<br>)

[//]: # ()
[//]: # (Note that the profiles don't have their Twitter keys set. This is, for now, a mandatory setting, and so)

[//]: # ()
[//]: # (```python)

[//]: # (>>> p.validate&#40;&#41;)

[//]: # (```)

[//]: # (```bash)

[//]: # (ValueError: Values not set for the following Twitter keys: ['Consumer Key', 'Consumer Secret', 'Access Token', 'Token Secret'])

[//]: # (```)

[//]: # ()
[//]: # (## The User Map)

[//]: # ()
[//]: # (#### The ```user_map``` allows a {py:class}`~.InstaTweet.Profile` to maintain a history of package-related activity for the Instagram users you've added)

[//]: # ()
[//]: # ()
[//]: # (#### Users are mapped to their ```USER_MAPPING```, which contains their associated lists of:)

[//]: # ()
[//]: # (https://github.com/TDKorn/insta-tweet/blob/74fbbed30376c67eb327297bbb27fc0557c8229e/InstaTweet/profile.py#L27)

[//]: # ()
[//]: # (* ```hashtags``` — the user's associated hashtag list &#40;for use when composing tweets&#41;)

[//]: # (* ```scraped``` — the list of posts that have been scraped from the user &#40;only the post id&#41;)

[//]: # (* ```tweets``` — the list of sent tweets containing media scraped from that user &#40;limited data&#41;)

[//]: # ()
[//]: # ()
[//]: # (## Adding Users and Hashtags)

[//]: # (S)

[//]: # ()
[//]: # ()
[//]: # ()

[//]: # (# STUFF I NEED TO EDIT)

[//]: # ()
[//]: # (## Populating the User Map)

[//]: # ()
[//]: # (The user map is a mapping of Instagram usernames to their associated ```USER_MAPPING```)

[//]: # ()
[//]: # ()
[//]: # ()
[//]: # (<br>)

[//]: # ()
[//]: # (The mapping gets updated as InstaTweet runs, when posts are successfully scraped and tweeted from these users.)

[//]: # (The {py:class}`~.InstaTweet.Profile` has methods to easily access and modify these mappings)

[//]: # ()
[//]: # (### Adding Users)

[//]: # ()
[//]: # (Use the ```add_users&#40;&#41;``` method to add users to a Profile's user map)

[//]: # ()
[//]: # (```python)

[//]: # (from InstaTweet import Profile)

[//]: # ()
[//]: # (>>> p = Profile&#40;'myProfile'&#41;)

[//]: # (>>> p.add_users&#40;'username'&#41;)

[//]: # ()
[//]: # (Added Instagram user @username to the user map)

[//]: # ()
[//]: # (>>> usernames = ['user','names'])

[//]: # (>>> p.add_users&#40;usernames&#41;)

[//]: # ()
[//]: # (Added Instagram user @user to the user map)

[//]: # (Added Instagram user @names to the user map)

[//]: # ()
[//]: # (>>> p.view_config&#40;&#41;)

[//]: # (```)

[//]: # (```shell)

[//]: # (name : myProfile)

[//]: # (local : True)

[//]: # (session_id :)

[//]: # (twitter_keys : {'Consumer Key': 'string', 'Consumer Secret': 'string', 'Access Token': 'string', 'Token Secret': 'string'})

[//]: # (user_agent : Mozilla/5.0 &#40;Windows NT 10.0; Win64; x64&#41; AppleWebKit/537.36 &#40;KHTML, like Gecko&#41; Chrome/102.0.5005.63 Safari/537.36)

[//]: # (proxy_key : None)

[//]: # (user_map : {'username': {'hashtags': [], 'scraped': [], 'tweets': []}, 'user': {'hashtags': [], 'scraped': [], 'tweets': []}, 'names': {'hashtags': [], 'scraped': [], 'tweets': []}})

[//]: # (```)

[//]: # ()
[//]: # (You can use the ```get_user&#40;&#41;``` method to retrieve the mapping of a particular user)

[//]: # (```python)

[//]: # (>>> print&#40;p.get_user&#40;'names'&#41;&#41;)

[//]: # ()
[//]: # ({'hashtags': [], 'scraped': [], 'tweets': []})

[//]: # (```)

[//]: # (***)

[//]: # ()
[//]: # (### Adding Hashtags)

[//]: # (Use the ```add_hashtags&#40;&#41;``` method to add hashtags to a specific user in the Profile's user map)

[//]: # ()
[//]: # (```python)

[//]: # (>>> p.add_hashtags&#40;user='username', hashtags='cool'&#41;)

[//]: # ()
[//]: # (Added hashtags for @username)

[//]: # ()
[//]: # (>>> hashtags = ['wow', 'okay'])

[//]: # (>>> p.add_hashtags&#40;'user', hashtags&#41;)

[//]: # ()
[//]: # (Added hashtags for @user)

[//]: # ()
[//]: # (>>> print&#40;p.user_map&#41;)

[//]: # ({'username': {'hashtags': ['cool'], 'scraped': [], 'tweets': []}, 'user': {'hashtags': ['wow', 'okay'], 'scraped': [], 'tweets': []}, 'names': {'hashtags': [], 'scraped': [], 'tweets': []}})

[//]: # (```)

[//]: # ()
[//]: # (You can use the ```get_hashtags_for&#40;&#41;``` method to retrieve the hashtag list of a specific username)

[//]: # ()
[//]: # (```python)

[//]: # (>>> print&#40;p.get_hashtags_for&#40;'user'&#41;&#41;)

[//]: # ()
[//]: # (['wow', 'okay'])

[//]: # (```)

[//]: # ()
[//]: # (<br>)

[//]: # ()
[//]: # (## Saving a Profile)

[//]: # ()
[//]: # (The profile can be saved either locally or to a SQLAlchemy supported database -- just set the ```DATABASE_URL```)

[//]: # (environment variable)

[//]: # ()
[//]: # (> **NOTE:** Saving a `Profile` is not mandatory to run InstaTweet, but doing so allows for easy access to associated API)

[//]: # (settings as well as tracking of previously scraped & tweeted posts &#40;which is used to determine which posts are new&#41;    )

[//]: # ()
[//]: # ([//]: # &#40;&#41;)
[//]: # ([//]: # &#40;To run InstaTweet, it is mandatory to create and use a {py:class}`~.InstaTweet.Profile`. It doesn't need to be saved, but doing&#41;)
[//]: # ()
[//]: # ([//]: # &#40;so will allow you to easily keep track of which posts have been scraped and tweeted already, and, by extension,&#41;)
[//]: # ()
[//]: # ([//]: # &#40;which ones are new. &#41;)
[//]: # ()
[//]: # (Call ```save&#40;&#41;``` to save the profile using the current or specified profile ```name```. The value of ```local``` determines the location and save format)

[//]: # ()
[//]: # (* If ```local=True```, the profile will be saved as a pickle file in the ```Profile.LOCAL_DIR```)

[//]: # ()
[//]: # (* Otherwise, the profile will be saved to the database specified by the ```DATABASE_URL``` environment variable)

[//]: # (- It gets converted to a pickle byte string &#40;via ```to_pickle&#40;&#41;```&#41;, which is then used to add/update a row)

[//]: # ()
[//]: # (<br>)

[//]: # ()
[//]: # (https://github.com/TDKorn/insta-tweet/blob/dc904af214596588bfc75b32eccc1ff37d0c271b/InstaTweet/profile.py#L142-L147)

[//]: # ()
[//]: # (<br>)

[//]: # ()
[//]: # (#### Example:)

[//]: # (```python)

[//]: # (>>> p = Profile&#40;'myProfile'&#41;)

[//]: # (>>> p.save&#40;&#41;)

[//]: # ()
[//]: # (Saved Local Profile myProfile)

[//]: # (```)

[//]: # ()
[//]: # (<br>)

[//]: # ()
[//]: # (Note that you can specify a new name for the profile at the time of saving, but it still must be unique)

[//]: # ()
[//]: # (```python)

[//]: # (>>> q = Profile&#40;&#41;)

[//]: # (>>> q.save&#40;'aProfile'&#41;)

[//]: # ()
[//]: # (Saved Local Profile aProfile)

[//]: # ()
[//]: # (>>> q.save&#40;'myProfile'&#41;)

[//]: # ()
[//]: # (FileExistsError: Local save file already exists for profile named "myProfile")

[//]: # (Please choose another name, load the profile, or delete the file.)

[//]: # (```)

[//]: # ()
[//]: # (<br>)

[//]: # ()
[//]: # (You can see if a profile name already exists remotely or locally by calling the ```profile_exists&#40;&#41;``` static method:)

[//]: # ()
[//]: # (https://github.com/TDKorn/insta-tweet/blob/dc904af214596588bfc75b32eccc1ff37d0c271b/InstaTweet/profile.py#L79-L86)

[//]: # ()
[//]: # (<br>)
