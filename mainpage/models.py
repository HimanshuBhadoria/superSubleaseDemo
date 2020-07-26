from django.db import models
from django.contrib.auth.models import User
from model_utils import Choices

# Create your models here.
class Posting(models.Model):

    mfn = Choices('male', 'female', 'none')
    yfn = Choices('Yes', 'Fee', 'No')
    ypn = Choices('Yes', 'Partial', 'No')


    PostingID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    StreetAddress = models.CharField(max_length=255)
    NumberOfBedrooms = models.IntegerField()
    NumberOfBathrooms = models.IntegerField()
    Rent = models.IntegerField()
    GenderPreference = models.CharField(choices=mfn, max_length=20)
    PetsAllowed = models.CharField(choices=yfn, max_length=20)
    ParkingIncluded = models.CharField(choices=yfn, max_length=20)
    WasherDryerIncluded = models.CharField(choices=yfn, max_length=20)
    UtilitiesIncluded = models.CharField(choices=ypn, max_length=20)

    def __str__(self):
        return self.StreetAddress
