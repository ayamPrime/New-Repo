from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Listing(models.Model):
    listing_title = models.CharField(max_length = 100)
    class PropertyType(models.TextChoices):
        SELF_CONTAIN = 'self-contain'
        SINGLE_ROOM = 'single room'
        SHARED_ROOM = 'shared room'
        SHARED_APARTMENT = 'shared apartment'
    property_type = models.CharField(max_length = 20, choices = PropertyType.choices)
    rooms_available = models.PositiveIntegerField(validators = [MinValueValidator(0)])
    rent_price = models.DecimalField(max_digits = 10, decimal_places = 2, validators = [MinValueValidator(1000)])
    agent = models.ForeignKey(
        'accounts.CustomUser',
        on_delete = models.CASCADE,
        related_name = 'listings',
    )

    def __str__(self):
        return f" {self.listing_title}"

class Location(models.Model):
    listing = models.OneToOneField(
        Listing,
        on_delete = models.CASCADE,
        primary_key = True
    )
    str_address = models.CharField(max_length = 120)
    distance_desc = models.TextField(blank = True, help_text = "e.g. 5 minute walk to the Main Gate...")

    def __str__(self):
        return f"Location of {self.listing.listing_title}"

class Amenities(models.Model):
    listing = models.OneToOneField(
        Listing,
        on_delete = models.CASCADE,
        primary_key = True
    )
    has_water = models.BooleanField(default = False)
    has_electricity = models.BooleanField(default = False)
    has_security = models.BooleanField(default = False)
    has_bathroom = models.BooleanField(default = False)
    has_kitchen = models.BooleanField(default = False)
    has_parking = models.BooleanField(default = False)
    has_fence = models.BooleanField(default = False)
    has_prepaid = models.BooleanField(default = False)

    def __str__(self):
        return f"Amenity list for {self.listing.listing_title}"

class ListingImage(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete = models.CASCADE,
        related_name = 'images'
    )
    image = models.ImageField(upload_to = 'listings/images/')

    def __str__(self):
        return f"Image for {self.listing.listing_title}"
    
class ListingVideo(models.Model):
    listing = models.OneToOneField(
        Listing,
        on_delete=models.CASCADE,
        related_name='video'
    )
    video = models.FileField(upload_to='listings/videos/', blank=True)

    def __str__(self):
        return f"Video for {self.listing.listing_title}"
    
class ListingFlag(models.Model):
    class Reason(models.TextChoices):
        FAKE = 'fake', 'Fake or fraudulent listing'
        WRONG_PRICE = 'wrong_price', 'Price is incorrect'
        ALREADY_TAKEN = 'already_taken', 'Room is no longer available'
        WRONG_LOCATION = 'wrong_location', 'Location is incorrect'
        INAPPROPRIATE = 'inappropriate', 'Inappropriate content'
        OTHER = 'other', 'Other'

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='flags'
    )
    flagged_by = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='flags_made'
    )
    reason = models.CharField(max_length=20, choices=Reason.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # One flag per user per listing — prevents spam flagging
        unique_together = ('listing', 'flagged_by')

    def __str__(self):
        return f"{self.listing.listing_title} flagged for {self.reason}"