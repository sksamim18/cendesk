from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=10, unique=True)
    pan_card = models.FileField(null=True)
    bank_details = models.FileField(null=True)
    aadhar_details = models.FileField(null=True)
    photo = models.FileField(null=True)
    active = models.BooleanField(default=False)
    document_submitted = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']

    def __str__(self):
        return 'Phone number: {}, First name {}, Last name: {}'.format(
            self.username,
            self.first_name,
            self.last_name
        )

    @property
    def get_phone_number(self):
        return self.username

    @property
    def get_full_name(self):
        full_name = self.first_name
        if self.first_name:
            full_name += self.first_name
        if self.last_name:
            full_name += self.last_name
        return full_name

    class Meta:
        ordering = ['username']


class Otp(models.Model):
    phone_number = models.CharField(max_length=50)
    otp = models.CharField(max_length=5)
