import random
import threading
from django.shortcuts import render
from account.forms import (
    RegistrationForm, LoginForm, ConfirmOtp, ClientUploadFileForm)
from django.http import HttpResponseRedirect
from account.models import Otp, Account
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login

from django.core.mail import send_mail
from django.conf import settings
from utils.tools import login_required
from django.contrib.auth import logout


def authentication(request):
    form = LoginForm()

    if request.method == 'POST':
        username = request.POST.get('phone_number')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if not user.active:
                return HttpResponseRedirect('/user/confirm_otp/')
            elif not user.document_submitted:
                return HttpResponseRedirect('/user/upload_docs/')
            else:
                return HttpResponseRedirect('/dashboard/')
        else:
            err = 'Could not login. Check your email and password.'
            return render(request, 'account/login.html', {'form': form, 'error': err})

    return render(request, 'account/login.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            phone_number = request.POST.get('username')
            password = request.POST.get('password')
            otp = random.randint(10000, 99999)
            otp_instance = Otp(phone_number=phone_number, otp=otp)
            otp_instance.save()
            thread = threading.Thread(
                target=send_email,
                args=(email, otp)
            )
            thread.start()
            user_instance = form.save(commit=True)
            user_instance.set_password(password)
            user_instance.save()
            return HttpResponseRedirect('/user/confirm_otp')
    else:
        form = RegistrationForm()
    return render(request, 'account/registration.html', {'form': form})


def send_email(email, otp):
    subject = 'Thank you for registering to our site'
    message = 'Your otp is {}'.format(otp)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return


def confirm_otp(request):
    context = {}
    context['form'] = ConfirmOtp()

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        otp = request.POST.get('otp')
        otp_instance = Otp.objects.filter(
            phone_number=phone_number, otp=otp).first()
        if otp_instance:
            otp_instance.delete()
            user = Account.objects.get(username=phone_number)
            user.active = True
            user.save()
            return HttpResponseRedirect('/user/login/')
        else:
            context['error'] = 'Wrong Otp Passed'

    return render(request, 'account/confirm_otp.html', context)


@login_required
def upload_docs(request):
    context = {}
    context['form'] = ClientUploadFileForm
    if request.method == 'POST':
        for field, image in request.FILES.items():
            upload_single_file(image, field, request)
        user = request.user
        user.document_submitted = True
        user.save()
        return HttpResponseRedirect('/dashboard/')
    return render(request, 'account/upload_docs.html', context)


def upload_single_file(file, field, request):
    import uuid
    file_ext = file.name.split('.')[-1]
    file_name = file.name.split('.')[-2]
    cleaned_file_name = file_name + ''.join(
        str(uuid.uuid4()).split('-')) + '.' + file_ext
    fs = FileSystemStorage()
    filename = fs.save(cleaned_file_name, file)
    uploaded_file_url = fs.url(filename)
    uploaded_file_url = uploaded_file_url.replace('/media/', '')
    user = request.user
    setattr(user, field, uploaded_file_url)
    user.save()


def sign_out(request):
    logout(request)
    return HttpResponseRedirect('/')
