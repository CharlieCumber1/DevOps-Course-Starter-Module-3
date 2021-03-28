from flask_login import UserMixin

writers = ['CharlieCumber1']

class User(UserMixin):
    def __init__(self, username):
        self.id = username

    def is_writer(self):
        return self.id in writers
