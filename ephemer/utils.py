from contextlib import contextmanager

from django.contrib.auth import models as auth

########################################################################
# Test helpers
########################################################################


@contextmanager
def login(client, is_staff=False, username="test", email="test@example.com"):
    """Create a user and sign her into the application"""
    user = auth.User.objects.create_user(
        username=username, email=email, is_staff=is_staff
    )
    client.force_login(user)
    yield user
