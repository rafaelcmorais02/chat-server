class UserServices:
    @staticmethod
    def returnAllUser(users, id):
        new_users = []
        for user in users:
            if user['id'] != id:
                new_users.append(user)
        return new_users
