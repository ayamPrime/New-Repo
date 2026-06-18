from django import forms
from .models import Listing, Location, Amenities, ListingImage, ListingVideo

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['listing_title', 'property_type', 'rooms_available', 'rent_price']

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['str_address', 'distance_desc']

class AmenitiesForm(forms.ModelForm):
    class Meta:
        model = Amenities
        fields = ['has_water', 'has_electricity', 'has_security', 'has_bathroom', 'has_kitchen', 'has_parking', 'has_fence', 'has_prepaid']

class ListingImageForm(forms.ModelForm):
    class Meta:
        model = ListingImage
        fields = ['image']

class ListingVideoForm(forms.ModelForm):
    class Meta:
        model = ListingVideo
        fields = ['video']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['video'].required = False