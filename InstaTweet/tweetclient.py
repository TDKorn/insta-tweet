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

    @staticmethod
    def default_keys():
        return {
            'Consumer Key': None,
            'Consumer Secret': None,
            'Access Token': None,
            'Token Secret': None
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
        self.video_path = post.file_path
        # For twitter media upload
        self.media_id = None
        self.processing_info = None

    @property
    def total_bytes(self):
        return os.path.getsize(self.video_path)

    def send(self):
        if self.post.is_video:
            self.crop_video()

        self._media_upload_init()
        self._media_upload_append()
        self._media_upload_finalize()
        self.post.tweet = self._post_tweet()
        os.remove(self.video_path)

    def crop_video(self):
        clip = VideoFileClip(self.video_path)
        bbox = self._get_bbox(clip)

        if bbox:
            new_path = self.video_path.replace('.mp4', '_cropped.mp4')
            cropped_clip = crop(clip, x1=bbox[0], y1=bbox[1], x2=bbox[2], y2=bbox[3])
            cropped_clip.write_videofile(new_path, audio_codec='aac')
            cropped_clip.close()
            os.remove(self.video_path)  # Delete uncropped video
            self.video_path = new_path

        clip.close()

    def _get_bbox(self, clip):
        frame_path = self.video_path.replace('.mp4', '_frame.png')
        clip.save_frame(frame_path)
        img = Image.open(frame_path)
        bbox = img.getbbox()
        img.close()
        os.remove(frame_path)
        return bbox

    def _media_upload_init(self):
        request_data = {
            'command': 'INIT',
            'media_type': mimetypes.guess_type(self.video_path)[0],
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
        file = open(self.video_path, 'rb')

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
            return r.json()
        print(r.json())

    def _build_tweet(self):
        link = self.post.permalink
        caption = self.post.caption.strip().replace('@', '@/')  # Avoid tagging randos on Twitter

        if self.hashtags:
            random_hashtags = random.sample(self.hashtags, random.choice(min([4, 5], [len(self.hashtags)] * 2)))
            hashtags = ' '.join(f'#{hashtag}' for hashtag in random_hashtags)
            return '\n'.join((caption, hashtags, '', link))
        return '\n'.join((caption, '', link))
