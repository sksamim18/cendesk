from django import forms
from django.forms import ModelForm
from taxmust.models import Contact, Service


class AddContactForm(ModelForm):
    customer_name = 'Enter customer full name'
    email = 'Enter customer email ID'
    phone_number = 'Enter phone number'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer_name'].widget.attrs['class'] = 'form-control'
        self.fields['customer_name'].widget.attrs['placeholder'] = self.customer_name
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = self.email
        self.fields['phone_number'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['placeholder'] = self.phone_number

    class Meta:
        model = Contact
        fields = ('customer_name', 'email', 'phone_number')


class AddServiceForm(forms.Form):
    all_services = Service.objects.all()
    choices = [(service.id, service.name) for service in all_services]
    service_name = forms.ChoiceField(choices=choices)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_name'].widget.attrs['class'] = 'form-control'


class DocumentUploadFileForm(forms.Form):
    title = forms.CharField()
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['placeholder'] = 'Ex. Aadhar Card'
        self.fields['file'].widget.attrs['class'] = 'form-control'
