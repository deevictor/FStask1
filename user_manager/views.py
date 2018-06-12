from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from smtplib import SMTPException
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, ContactForm, ContactAdminsForm
from django.conf import settings
from django.core.mail import send_mail, mail_admins
from .models import Notification

# Create your views here.

def home(request):
    return render(request, 'base.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = raw_password)
            login(request, user)
            messages.info(request, "thanks for registering. Please login to continue.")
            return JsonResponse({'status': 'success', 'url': '/'})

    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_user(request):
    form = AuthenticationForm(request.POST)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'url': '/'})
        else:
            return JsonResponse({'status': 'fail', 'url': '/'})

    return render(request, 'login.html', {'form': form})

@login_required
def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            # for key, value in form.cleaned_data.items():
            #     print(key, value)
            form_email = form.cleaned_data.get('email')
            form_message = form.cleaned_data.get('message')
            # form_username = form.cleaned_data.get('username')
            subject = 'Site contact form'
            from_email = settings.EMAIL_HOST_USER
            to_email = [form_email]
            contact_message = form_message
            # print(to_email, from_email)
            send_mail(subject,
                      contact_message,
                      from_email,
                      to_email,
                      fail_silently=False)
            return JsonResponse({'status': 'success', 'url': '/'})
        else:
            return JsonResponse({'status': 'fail', 'url': '/'})

    context = {
    "form": form,
    }
    return render(request, "messaging/message.html", context)

@login_required
def contact_admins(request):
    form = ContactAdminsForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            # for key, value in form.cleaned_data.items():
            #     print(key, value)
            # form_email = form.cleaned_data.get('email')
            form_message = form.cleaned_data.get('message')
            # form_username = form.cleaned_data.get('username')
            form_subject = form.cleaned_data.get('subject')
            # from_email = settings.EMAIL_HOST_USER
            # to_email = [form_email]
            subject = form_subject
            contact_message = form_message
            # print(to_email, from_email)
            notification = Notification()
            notification.message = contact_message[:200]
            notification.sender = request.user.email
            notification.status = 'message sent'

            try:
                mail_admins(subject,
                            contact_message,
                            fail_silently=False,
                            connection=None,
                            html_message=None)
                return JsonResponse({'status': 'success', 'url': '/'})

            except SMTPException as e:
                notification.status = 'There was an error sending an email'
                print(notification.status, e)
                return JsonResponse({'status': 'fail', 'url': '/'})

            finally:
                notification.save()

    context = {
    "form": form
    }
    return render(request, "messaging/message.html", context)
