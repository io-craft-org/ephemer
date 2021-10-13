from django import forms


class RegisterForm(forms.Form):
    """Form to register a new User"""

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()


class ContactForm(forms.Form):
    firstname = forms.CharField(max_length=256, label="Prénom")
    lastname = forms.CharField(max_length=256, label="Nom")
    email = forms.EmailField(max_length=254, label="Email")
    subject = forms.CharField(max_length=256, label="Objet")
    content = forms.CharField(max_length=2048, widget=forms.Textarea, label="Message")
