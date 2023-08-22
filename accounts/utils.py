from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.id}{timestamp}{user.is_verified}{user.is_active}"


token_generator = TokenGenerator()


def custom_user_display(user):
    return user.email

