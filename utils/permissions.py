from functools import wraps


def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):

            if not self.user_session.has_permission(permission):
                raise PermissionError(f"Permission refusée : {permission}")

            return func(self, *args, **kwargs)

        return wrapper
    return decorator
