from django import forms
from .models import Listing, Location, Amenities, ListingImage, ListingVideo, ListingFlag

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['listing_title', 'property_type', 'rooms_available', 'rent_price']
        widgets = {
            'listing_title': forms.TextInput(attrs={'placeholder': 'e.g. 3 Bedroom Self-Contain at Oru'}),
        }

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['str_address', 'distance_desc']

class AmenitiesForm(forms.ModelForm):
    class Meta:
        model = Amenities
        fields = ['has_water', 'has_electricity', 'has_security', 'has_bathroom', 'has_kitchen', 'has_parking', 'has_fence', 'has_prepaid']

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        default_attrs = {'multiple': True, 'accept': 'image/*'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def value_from_datadict(self, data, files, name):
        upload = files.getlist(name)
        if not upload:
            return files.get(name)
        return upload

class MultipleImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        return single_file_clean(data, initial)

class ListingImagesForm(forms.Form):
    images = MultipleImageField(required=True)

class ListingVideoForm(forms.ModelForm):
    class Meta:
        model = ListingVideo
        fields = ['video']
        widgets = {
            'video': forms.ClearableFileInput(attrs={'accept': 'video/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['video'].required = False
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['video'].required = False

class ListingFlagForm(forms.ModelForm):
    class Meta:
        model = ListingFlag
        fields = ['reason']