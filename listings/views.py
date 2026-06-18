from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import ListingForm, LocationForm, AmenitiesForm, ListingImageForm, ListingVideoForm
from .models import Listing

# Create your views here.
def home_page(request):
    listings = Listing.objects.order_by('-id')[:3]
    return render(request, 'listings/index.html', {'listings': listings})

def listings_page(request):
    listings = Listing.objects.all()
    return render(request, 'listings/listings.html', {'listings': listings})

@login_required
def add_listings(request):
    if request.user.account_type != 'agent':
        redirect('home')

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        form1 = LocationForm(request.POST)
        form2 = AmenitiesForm(request.POST)
        form3 = ListingImageForm(request.POST, request.FILES)
        form4 = ListingVideoForm(request.POST, request.FILES)
    if request.method == 'POST':
            listing = form.save(commit=False)
            listing.agent = request.user
            listing.save()

            location = form1.save(commit=False)
            location.listing = listing
            location.save()

            amenities = form2.save(commit=False)
            amenities.listing = listing
            amenities.save()

            image = form3.save(commit=False)
            image.listing = listing
            image.save()

            video = form4.save(commit=False)
            video.listing = listing
            if request.FILES.get('video'):
                video.save()

            return redirect('profile')
    else:
        form = ListingForm()
        form1 = LocationForm()
        form2 = AmenitiesForm()
        form3 = ListingImageForm()
        form4 = ListingVideoForm()
    return render(request, 'listings/add_listings.html', {
        'listing_form': form,
        'location_form': form1,
        'amenities_form': form2,
        'image_form': form3,
        'video_form': form4,
    })

def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'listings/listing_details.html', {'listing': listing})