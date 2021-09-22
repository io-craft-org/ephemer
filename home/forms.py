from django import forms


class RegisterForm(forms.Form):
    """Form to register a new User"""

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
