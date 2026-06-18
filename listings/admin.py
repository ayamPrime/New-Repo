from django.contrib import admin
from .models import Listing, Location, Amenities, ListingImage, ListingVideo

# Register your models here.
admin.site.register(Listing)
admin.site.register(Location)
admin.site.register(Amenities)
admin.site.register(ListingImage)
admin.site.register(ListingVideo)