class Comment:
    def __init__(self, comment_json):
        self.message = comment_json['message']
        self.id = comment_json['id']
