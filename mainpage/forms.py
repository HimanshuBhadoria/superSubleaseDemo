from django.forms import ModelForm
from .models import Posting

class PostingForm(ModelForm):
    class Meta:
        model = Posting
        fields = ['StreetAddress', 'NumberOfBedrooms', 'NumberOfBathrooms', 'Rent', 'GenderPreference', 'PetsAllowed', 'ParkingIncluded', 'WasherDryerIncluded', 'UtilitiesIncluded']
