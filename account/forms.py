from django import forms
from django.forms import PasswordInput
from django.forms import ModelForm
from account.models import Account


class RegistrationForm(ModelForm):
    name = 'Enter your full name'
    email = 'Enter your email ID'
    phone_number = 'Enter your phone number'
    password = 'Enter your password'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = self.name
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = self.email
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = self.phone_number

    class Meta:
        model = Account
        fields = ('name', 'email', 'username', 'password')
        widgets = {
            'password': PasswordInput(
                attrs={'class': 'form-control', 'placeholder':
                       'Enter your password'})
        }


class LoginForm(forms.Form):
    phone_number = forms.CharField()
    password = forms.CharField(widget=PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs[
            'class'] = 'form-control'
        self.fields['phone_number'].widget.attrs[
            'placeholder'] = 'Enter your phone number'


class ConfirmOtp(forms.Form):
    phone_number = forms.CharField()
    otp = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs[
            'placeholder'] = 'Enter your phone number'
        self.fields['otp'].widget.attrs['class'] = 'form-control'
        self.fields['otp'].widget.attrs['placeholder'] = 'Enter your Otp'


class ClientUploadFileForm(forms.Form):
    bank_details = forms.FileField()
    aadhar_details = forms.FileField()
    photo = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bank_details'].widget.attrs['class'] = 'form-control'
        self.fields['aadhar_details'].widget.attrs['class'] = 'form-control'
        self.fields['photo'].widget.attrs['class'] = 'form-control'



