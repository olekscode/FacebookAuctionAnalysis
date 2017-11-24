class RequestURL:
    def __init__(self, access_token):
        self.template_url = \
            'https://graph.facebook.com/v2.11/'\
            '{}/{}?limit=200&access_token={}'
            
        self.simple_template_url =\
            'https://graph.facebook.com/v2.11/{}?access_token={}'

        self.template_url = self.template_url.format('{}', '{}', access_token)
        self.simple_template_url = self.simple_template_url.format('{}', access_token)

    def photos_in_album(self, album_id):
        return self.template_url.format(album_id, 'photos')
    
    def photo(self, photo_id):
        return self.simple_template_url.format(photo_id)

    def comments_on_photo(self, photo_id):
        return self.template_url.format(photo_id, 'comments')

    def tags_on_photo(self, photo_id):
        return self.template_url.format(photo_id, 'tags')
