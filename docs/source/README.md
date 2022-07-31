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

With `InstaTweet`, you can rest easy knowing that, although nobody will click the link, they'll at least see what you posted.

<br>

## What's InstaTweet?

`InstaTweet` is a tool that automatically reposts content from Instagram to Twitter.

Simply create a {py:class}`~.InstaTweet.Profile`, configure the 
{ref}`required settings <mandatory-settings>`, and {py:meth}`~.add_users` to repost from.
Then {py:meth}`~.InstaTweet.load` it into an {py:class}`~.InstaTweet` object and call {py:meth}`~.start`

```python
from InstaTweet import InstaTweet

# Load and InstaTweet a locally saved Profile
insta_tweet = InstaTweet.load('myProfile')
insta_tweet.start()
```

`InstaTweet` will scrape the added users most recent Instagram {py:attr}`~.posts`, and if any are new,
they'll be automatically downloaded and reposted to Twitter.


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

You can easily schedule InstaTweet using the provided [scheduler](https://github.com/tdkorn/insta-tweet/blob/2.0.0/scheduler.py) 
script

```{literalinclude} ../../scheduler.py
```
https://github.com/TDKorn/insta-tweet/blob/1d862bf0c7d04109f5b9e1fe0cb39ac78ed4b114/scheduler.py#L1-L19

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
## Create a New Profile

When creating a {py:class}`~.Profile`, all settings can be passed as arguments at the point of initialization or
set directly as object attributes anytime after

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

```{note}
* Property setters validate data types for the mandatory settings
* Requirements aren't strictly enforced until {py:meth}`.InstaTweet.start` is called, 
which will first {py:meth}`~.Profile.validate` the profile 
```

You can view all settings via the {py:attr}`~.config` dict, or the {py:meth}`~.view_config` method 
for a legible version

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


