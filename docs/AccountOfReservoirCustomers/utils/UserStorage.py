class UserStorage:
    users_list = {}

    def __init__(self, user_id: int, obj: object):
        self.users_list[user_id] = obj


