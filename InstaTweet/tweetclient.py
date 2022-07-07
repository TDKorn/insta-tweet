import os
import sys
import time
import random
import requests
import mimetypes
from PIL import Image
from requests_oauthlib import OAuth1
from moviepy.video.fx.crop import crop
from moviepy.video.io.VideoFileClip import VideoFileClip

MEDIA_ENDPOINT_URL = 'https://upload.twitter.com/1.1/media/upload.json'
POST_TWEET_URL = 'https://api.twitter.com/1.1/statuses/update.json'


class TweetClient(object):

    DEFAULT_KEYS = {
        'Consumer Key': 'string',
        'Consumer Secret': 'string',
        'Access Token': 'string',
        'Token Secret': 'string'
    }

    @staticmethod
    def oauth(keys):
        return OAuth1(
            keys['Consumer Key'],
            client_secret=keys['Consumer Secret'],
            resource_owner_key=keys['Access Token'],
            resource_owner_secret=keys['Token Secret']
        )

    def __init__(self, post, auth, hashtags=None):
        self.post = post
        self.auth = auth
        self.hashtags = hashtags
        self.media_path = post.filepath
        # For twitter media upload
        self.media_id = None
        self.processing_info = None

    @property
    def total_bytes(self):
        return os.path.getsize(self.media_path)

    def send(self):
        if self.post.is_video:
            print(f'Cropping video {self.post.id}')
            self.crop_video()

        self._media_upload_init()
        self._media_upload_append()
        self._media_upload_finalize()
        self.post.tweet = self._post_tweet()

        print(f'Tweet sent for post {self.post.id}')
        os.remove(self.media_path)

    def crop_video(self):
        clip = VideoFileClip(self.media_path)
        bbox = self._get_bbox(clip)

        if bbox:
            new_path = self.media_path.replace('.mp4', '_cropped.mp4')
            with crop(clip, x1=bbox[0], y1=bbox[1], x2=bbox[2], y2=bbox[3]) as cropped_clip:
                cropped_clip.write_videofile(new_path, audio_codec='aac', logger=None)

            os.remove(self.media_path)  # Delete uncropped video
            self.media_path = new_path

        clip.close()

    def _get_bbox(self, clip):
        frame_path = self.media_path.replace('.mp4', '_frame.png')
        clip.save_frame(frame_path)
        img = Image.open(frame_path)
        bbox = img.getbbox()
        img.close()
        os.remove(frame_path)
        return bbox

    def _media_upload_init(self):
        request_data = {
            'command': 'INIT',
            'media_type': mimetypes.guess_type(self.media_path)[0],
            'total_bytes': self.total_bytes,
            'media_category': 'TWEET_VIDEO' if self.post.is_video else 'TWEET_IMAGE'
        }

        r = requests.post(MEDIA_ENDPOINT_URL, data=request_data, auth=self.auth)
        if r.ok:
            self.media_id = r.json()['media_id']
        else:
            print('Failed to initialize Twitter media upload.', r.status_code, r.reason, sep='\n')
            sys.exit(0)

    def _media_upload_append(self):
        segment_id = 0
        bytes_sent = 0
        file = open(self.media_path, 'rb')

        while bytes_sent < self.total_bytes:
            chunk = file.read(4 * 1024 * 1024)
            request_data = {
                'command': 'APPEND',
                'media_id': self.media_id,
                'segment_index': segment_id
            }
            files = {'media': chunk}

            r = requests.post(MEDIA_ENDPOINT_URL, data=request_data, files=files, auth=self.auth)
            if r.status_code < 200 or r.status_code > 299:
                print(r.status_code)
                print(r.text)
                sys.exit(0)

            segment_id += 1
            bytes_sent = file.tell()

        print(f"Twitter media upload for post {self.post.id} complete")

    def _media_upload_finalize(self):
        request_data = {
            'command': 'FINALIZE',
            'media_id': self.media_id
        }

        r = requests.post(MEDIA_ENDPOINT_URL, data=request_data, auth=self.auth)
        if not r.ok:
            print(r.json())
            sys.exit(0)

        self.processing_info = r.json().get('processing_info', None)
        self._check_status()

    def _check_status(self):
        if not self.processing_info:
            return

        state = self.processing_info['state']
        if state == u'succeeded':
            return
        if state == u'failed':
            print(self.processing_info)
            sys.exit(0)

        wait = self.processing_info['check_after_secs']
        time.sleep(wait)

        request_params = {
            'command': 'STATUS',
            'media_id': self.media_id
        }

        r = requests.get(MEDIA_ENDPOINT_URL, params=request_params, auth=self.auth)
        self.processing_info = r.json().get('processing_info', None)
        self._check_status()

    def _post_tweet(self):
        request_data = {
            'status': self._build_tweet(),
            'media_ids': self.media_id
        }

        r = requests.post(POST_TWEET_URL, data=request_data, auth=self.auth)
        if r.ok:
            tweet_data = r.json()
            return {
                'link': f'https://twitter.com/i/web/status/{tweet_data["id"]}',
                'created_at': tweet_data['created_at'],
                'text': tweet_data['text'],
            }
        print(r.json())

    def _build_tweet(self):
        link = self.post.permalink
        caption = self.post.caption.strip().replace('@', '@/')  # Avoid tagging randos on Twitter
        characters = 295

        if self.hashtags:
            random_hashtags = random.sample(self.hashtags, random.choice(min([4, 5], [len(self.hashtags)] * 2)))
            hashtags = ' '.join(f'#{hashtag}' for hashtag in random_hashtags)
            characters -= (len(hashtags + link) + 3)    # For 3 newlines    ->  caption \n hashtags \n\n link
            tweet = '\n'.join((caption[:characters], hashtags, '', link))

        else:
            characters -= (len(link) + 2)       # For 2 newlines    ->  caption \n\n link
            tweet = '\n'.join((caption[:characters], '', link))

        return tweet
