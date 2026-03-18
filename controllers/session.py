class UserSession:
    def __init__(self, user):
        self.user = user
        self.is_authenticated = True

    def has_permission(self, permission: str):
        return getattr(self.user.departement, permission, False)

    def get_fullname(self):
        return f"{self.user.firstname} {self.user.name}"
