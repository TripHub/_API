from django.contrib.auth import get_user_model


class AdminEmailBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = get_user_model().objects.get(email=username)
            print('pwd', user.check_password(password))
            if user.check_password(password):
                print('success!', user)
                return user
        except get_user_model().DoesNotExist:
            pass
        return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
