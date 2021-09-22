from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView
from magicauth.next_url import NextUrlMixin
from magicauth.send_token import SendTokenMixin

from home.forms import RegisterForm


class Home(TemplateView):
    template_name = "home.html"


class RegisterOrLogin(TemplateView):
    template_name = "register_or_login.html"


class RegisterView(FormView, NextUrlMixin, SendTokenMixin):
    form_class = RegisterForm
    success_url = reverse_lazy("magicauth-email-sent")
    template_name = "home/register.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            next_url = self.get_next_url(self.request)
            return redirect(next_url)
        return super(RegisterView, self).get(request, *args, **kwargs)
