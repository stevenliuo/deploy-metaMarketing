from django.contrib.auth.tokens import PasswordResetTokenGenerator

import six


class ExpiringTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        hash_value = six.text_type(user.pk) + six.text_type(timestamp)

        return hash_value


class EmailExpiringTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        hash_value = six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)

        return hash_value


expiring_token_generation = ExpiringTokenGenerator()
email_expiring_token_generation = EmailExpiringTokenGenerator()
