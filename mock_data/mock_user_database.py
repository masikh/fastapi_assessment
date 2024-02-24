"""Mock user database"""


class MockUserDatabase:
    """Simple mock user database CRUD simulator"""

    def __init__(self):
        self.user_data = [
            {
                "_id": 0,
                "username": "admin",
                "full_name": "Admin",
                "email": "admin@example.com",
                "hashed_password": "$2b$12$B1jLytNj3vUxgrQ4TABeNOdVBxuJmXee0N6Cjf90m47XmB7YHHOHa",
                "disabled": False,
                "is_admin": True,
            }
        ]

    def get_user(self, username):
        """Get user from database by username"""

        for user in self.user_data:
            if user["username"] == username:
                return user
        return {}

    def add_user(self, user):
        """Add user to database"""

        self.user_data.append(user)

    def delete_user(self, username):
        """Delete user from database by username"""

        users = []
        for user in self.user_data:
            if user["username"] != username:
                users.append(user)
        self.user_data = users
        return True
