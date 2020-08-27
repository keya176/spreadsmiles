from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Organization(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    orgname = models.CharField(max_length=200, null=True)
    orgemail = models.CharField(max_length=200, null=True)
    orgcontact = models.CharField(max_length=200, null=True)
    orgaddress = models.CharField(max_length=200, null=True)
    orglicense = models.CharField(max_length=200, null=True)
    orgdate = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.orgname


class Event(models.Model):
    MONEY = 'MY'
    BELONGINGS = 'BL'
    BOTH = 'BH'
    EVENT_TYPE_CHOICES = [
        (MONEY, 'Money'),
        (BELONGINGS, 'Belongings'),
        (BOTH, 'Both'),
    ]
    event_type = models.CharField(
        max_length=2, choices=EVENT_TYPE_CHOICES, default=MONEY)
    organization_name = models.ForeignKey(
        Organization, null=True, on_delete=models.SET_NULL)
    cover = models.ImageField(default="f.jpg", null=True, blank=True)
    event_title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    goal = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    raised = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    belgoal = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_title


class MoneyDonatorInfo(models.Model):
    event = models.ForeignKey(
        Event, null=True, on_delete=models.SET_NULL, blank=True)
    organization = models.ForeignKey(
        Organization, null=True, on_delete=models.SET_NULL, blank=True)
    amount = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    name = models.CharField(max_length=264, blank=True)
    email = models.CharField(max_length=264, blank=True)
    contact = models.CharField(max_length=264, blank=True)
    opinion = models.TextField(max_length=500, blank=True)
    success_amount = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    val_id = models.CharField(max_length=264, null=True, blank=True)
    tran_id = models.CharField(max_length=264, null=True, blank=True)
    status = models.CharField(max_length=264, null=True, blank=True)

    def __str__(self):
        return self.name


class BelongingsDonatorInfo(models.Model):
    event = models.ForeignKey(
        Event, null=True, on_delete=models.SET_NULL, blank=True)
    organization = models.ForeignKey(
        Organization, null=True, on_delete=models.SET_NULL, blank=True)
    name = models.CharField(max_length=264, blank=True)
    email = models.CharField(max_length=264, blank=True)
    contact = models.CharField(max_length=264, blank=True)
    address = models.CharField(max_length=264, blank=True)
    opinion = models.TextField(max_length=500, blank=True)
    image = models.ImageField(null=True, blank=True)
    is_submitted = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name


class AdminPickup(models.Model):
    event = models.ForeignKey(
        Event, null=True, on_delete=models.SET_NULL, blank=True)
    organization = models.ForeignKey(
        Organization, null=True, on_delete=models.SET_NULL, blank=True)
    name = models.CharField(max_length=264, blank=True)
    email = models.CharField(max_length=264, blank=True)
    contact = models.CharField(max_length=264, blank=True)
    address = models.CharField(max_length=264, blank=True)
    opinion = models.TextField(max_length=500, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.organization.orgname


class Gallary(models.Model):
    image = models.ImageField(default="g.jpg", null=True, blank=True)
    des = models.CharField(default="SpreadSmile",
                           max_length=50, null=True, blank=True)

    def __str__(self):
        return self.image.name
