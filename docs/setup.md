## Settings

### Mandatory
- ```name``` -- Profile Name
- ```session_id``` -- Instagram Session Cookie
- ```twitter_keys``` -- Twitter v1.1 API Keys

### Mandatory with Default Values 
- ```local=True``` -- whether saves will be made locally or remotely
- ```user_agent=utils.get_agent()``` -- User Agent to use in requests

### Entirely Optional
- ```proxy_key``` -- environment variable to retrieve proxies from (for use in requests)

## Create a New Profile

Profiles can have their attributes set at initialization or any point afterwards
* For mandatory settings, data type validation is handled by property setters 
* The actual values of the data are validated when ```validate()``` is called
    - This method validates all settings to see if it's properly configured for InstaTweeting
    
```python
from InstaTweet import Profile
p = Profile()
p.name = 'tdk'
p.session_id = 'sessionid3209209'
p.add_users('dailykittenig')
p.add_hashtags('dailykittenig', ['cat','kitty','meow','purrrr'])
p.view_config()
p.save()
```
```shell
Added Instagram user @dailykittenig to the user map
Added hashtags for @dailykittenig
name : tdk
local : True
session_id : sessionid3209209
twitter_keys : {'Consumer Key': 'string', 'Consumer Secret': 'string', 'Access Token': 'string', 'Token Secret': 'string'}
user_agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36
proxy_key : None
user_map : {'dailykittenig': {'hashtags': ['purrrr', 'kitty', 'cat', 'meow'], 'scraped': [], 'tweets': []}}
Saved Local Profile tdk
```

```python
p.validate()
```
```shell
ValueError: Values not set for the following Twitter keys: ['Consumer Key', 'Consumer Secret', 'Access Token', 'Token Secret']
```

```python
p.local=False
p.save()
```

```shell
OSError: Must set the DATABASE_URL environment variable
```
# Setup on Heroku

## 1a) [Optional] Add Heroku Postgres add-on (or another SQLAlchemy supported db)

![image](https://user-images.githubusercontent.com/96394652/180402506-1decfb15-6729-4808-8b21-47872775c82b.png)
![image](https://user-images.githubusercontent.com/96394652/180402573-86293f1e-de0a-4d36-89f7-e3bcdf0e343e.png)
![image](https://user-images.githubusercontent.com/96394652/180402624-be1a9afe-95f2-4e13-afab-5aebab549f0a.png)
![image](https://user-images.githubusercontent.com/96394652/180402700-e8b537f4-a3b8-4329-acee-45e6e7904fec.png)


## 1b) Get the full URI of the database

### For Heroku Postgres you can find it in the `Settings`

![image](https://user-images.githubusercontent.com/96394652/180403276-92b7de8b-f3b6-47c4-bae7-52a78f8b5fab.png)

![image](https://user-images.githubusercontent.com/96394652/180403962-32374d13-6a63-4338-921c-0d61ff9dc736.png)
![image](https://user-images.githubusercontent.com/96394652/180404611-87474371-d606-455f-81ca-7c9c67b6119f.png)

## 2 Deploy your repo that uses InstaTweet and schedule with Heroku Scheduler





![image](https://user-images.githubusercontent.com/96394652/180407760-79869f8a-a06f-4f67-87b1-6a243735c130.png)
![image](https://user-images.githubusercontent.com/96394652/180407814-031e4fcb-ca82-48a4-b4bf-c74506226881.png)
![image](https://user-images.githubusercontent.com/96394652/180415715-ffb6df79-9c44-4c6c-83a6-abae5bc24dfe.png)
![image](https://user-images.githubusercontent.com/96394652/180415834-5f563274-0a1b-49c2-95a5-665244489c67.png)
![image](https://user-images.githubusercontent.com/96394652/180415921-369d71c9-959d-4e8c-8ae4-1d6b2897f291.png)
![image](https://user-images.githubusercontent.com/96394652/180415956-13d5a719-21d3-46d5-8bda-79914e1f4af7.png)
![image](https://user-images.githubusercontent.com/96394652/180416713-fa2cea9e-2e21-49f4-b55f-4537a7f2b0cd.png)

I really made a kussy fusion emoji.. by accident?????

![image](https://user-images.githubusercontent.com/96394652/180417279-91f38bd0-c70c-47b8-9c1e-f59f89425f90.png)

**WHY ARE THEY OVERLAPPED**

![image](https://user-images.githubusercontent.com/96394652/180417821-9e2534fc-75a8-4ab0-9f24-6ec197bedc65.png)

HEROKU PYTHON CONSOLE EXPLAIN YOURSELF??????

![image](https://user-images.githubusercontent.com/96394652/180430454-fc4cf523-d191-4bf0-8c2e-7ce010b72fce.png)
![image](https://user-images.githubusercontent.com/96394652/180433266-a4c4b5ff-1990-4ece-813d-7a8b6f27687d.png)
