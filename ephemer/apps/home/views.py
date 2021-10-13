import django.core.mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from ephemer.apps.home.forms import RegisterForm
from magicauth.next_url import NextUrlMixin
from magicauth.send_token import SendTokenMixin

from .forms import ContactForm


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


def faq(request):
    return render(
        request,
        template_name="faq.html",
    )


def guide(request):
    return render(
        request,
        template_name="guide.html",
    )


def contact(request):
    """Sends an email to the team with contact info from user"""
    next_url = request.GET.get("next", "/")
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            status = send_message_to_team(request, form.cleaned_data)
            notify_user_of_sending(request, status)
            return redirect(next_url)
    else:
        form = ContactForm()
    return render(request, "contact.html", locals())


def send_message_to_team(request, data):
    """Send message as email to the team"""
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    email = data.get("email")
    subject = data.get("subject")
    content = data.get("content")

    content += f"\n\nfrom: {firstname} {lastname} <{email}>"

    return django.core.mail.send_mail(
        subject=subject,
        message=content,
        from_email=settings.EMAIL_FROM,
        recipient_list=settings.TEAM_EMAILS,
        fail_silently=True,
    )


def notify_user_of_sending(request, status):
    """Notify user of sending request through message framework"""
    if status:
        messages.success(
            request, "Merci, votre demande a été transmis à l'équipe Ephemer !"
        )
    else:
        messages.error(
            request,
            "Désolé, nous n'avons pas réussi à envoyer votre courriel. "
            "Vous pouvez réessayer "
            "ou utiliser l'adresse depuis votre logiciel de messagerie",
        )
