# encoding: utf-8

"""
Utilities for home application
"""

from django import forms
from django.contrib.auth import models as auth


def create_user(email=None):
    """Create a new user if no one exists with given email"""
    if not email:
        raise forms.ValidationError("Adresse email non reconnue")
    auth.User.objects.create_user(email=email, username=email)
