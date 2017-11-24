import json
import requests

from request_url import RequestURL
from comment import Comment
from user import User


class DataLoader:
    def __init__(self, access_token):
        self.request_url = RequestURL(access_token)

    def get_participants(self, album_id):
        photo_ids = self._get_photo_ids(album_id)
        users = []

        for photo_id in photo_ids:
            tag_json = self._get_tag(photo_id)
            
            if tag_json != '':
                name = tag_json['name']
                
                if 'id' in tag_json.keys():
                    user_id = tag_json['id']
                else:
                    user_id = ''
                    
            else:
                name = ''
                user_id = ''
            
            description = self._get_description(photo_id)
            comments = self._get_comments(photo_id)
            likes = None

            u = User(name, user_id, description, comments, likes)
            users.append(u)
        
        return users

    def _get_photo_ids(self, album_id):
        url = self.request_url.photos_in_album(album_id)

        data = self._get_data_from_all_pages(url)
        return [photo['id'] for photo in data]
    
    def _get_description(self, photo_id):
        url = self.request_url.photo(photo_id)
        response = json.loads(requests.get(url).text)
        
        if 'name' in response.keys():
            return response['name']
        else:
            return ''

    def _get_comments(self, photo_id):
        url = self.request_url.comments_on_photo(photo_id)

        data = self._get_data_from_all_pages(url)
        return [Comment(item) for item in data]

    def _get_tag(self, photo_id):
        url = self.request_url.tags_on_photo(photo_id)

        r = requests.get(url)
        tag_json = json.loads(r.text)['data']

        if len(tag_json) > 0:
            return tag_json[0]
        else:
            return ''

    def _get_data_from_all_pages(self, url):
        data = []

        response = json.loads(requests.get(url).text)
        data += response['data']

        if ('paging' in response.keys()) and\
                ('next' in response['paging'].keys()):
            url = response['paging']['next']
            data += self._get_data_from_all_pages(url)

        return data
