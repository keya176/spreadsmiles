from django.db import models

# Create your models here.


class Organization(models.Model):
    orgname = models.CharField(max_length=200, null=True)
    orgemail = models.CharField(max_length=200, null=True)
    orgcontact = models.CharField(max_length=200, null=True)
    orgaddress = models.CharField(max_length=200, null=True)
    orglicense = models.CharField(max_length=200, null=True)
    orgdate = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.orgname


class Event(models.Model):
    organization_name = models.ForeignKey(
        Organization, null=True, on_delete=models.SET_NULL)
    event_title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_title