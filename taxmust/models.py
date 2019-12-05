from django.db import models
from account.models import Account
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class RootCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class ParentCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    root_category = models.ForeignKey(RootCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Service(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    parent_category = models.ForeignKey(
        ParentCategory, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Contact(models.Model):
    customer_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=50)
    client = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{} - {}'.format(
            self.phone_number, self.customer_name)

    class Meta:
        ordering = ['phone_number']


class Order(models.Model):
    CHOICES = (
        (1, 'APPLIED'),
        (2, 'ACCEPTED'),
        (3, 'IN PROGRESS'),
        (4, 'COMPLETED')
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    customer = models.ForeignKey(Contact, on_delete=models.CASCADE)
    status = models.IntegerField(choices=CHOICES, default=1)
    payment_status = models.BooleanField(default=False)
    payment_ID = models.CharField(max_length=100)

    @property
    def documents(self):
        return self.document_set.all()

    def __str__(self):
        return str(self.id)


class Document(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField()
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.file.url
