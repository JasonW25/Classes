class Post:
    def __init__(self, blog):
        self.id = blog['id']
        self.title = blog['title']
        self.subtitle = blog['subtitle']
        self.body = blog['body']
        self.image = blog['image']
        