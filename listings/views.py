from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ListingForm, LocationForm, AmenitiesForm, ListingImageForm, ListingVideoForm, ListingFlagForm
from .models import Listing, ListingFlag

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
        return redirect('home')

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        form1 = LocationForm(request.POST)
        form2 = AmenitiesForm(request.POST)
        form3 = ListingImageForm(request.POST, request.FILES)
        form4 = ListingVideoForm(request.POST, request.FILES)
        if form.is_valid() and form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
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

@login_required
def flag_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    # Prevent flagging your own listing
    if request.user == listing.agent:
        messages.error(request, "You cannot report your own listing.")
        return redirect('listing_detail', pk=pk)

    # Prevent duplicate flags from the same user
    if ListingFlag.objects.filter(listing=listing, flagged_by=request.user).exists():
        messages.error(request, "You have already reported this listing.")
        return redirect('listing_detail', pk=pk)

    if request.method == 'POST':
        form = ListingFlagForm(request.POST)
        if form.is_valid():
            flag = form.save(commit=False)
            flag.listing = listing
            flag.flagged_by = request.user
            flag.save()
            messages.success(request, "Thank you. Your report has been submitted.")
            return redirect('listing_detail', pk=pk)
    else:
        form = ListingFlagForm()

    return render(request, 'listings/flag_listing.html', {
        'form': form,
        'listing': listing,
    })


def inspection_placeholder(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'listings/coming_soon.html', {
        'feature': 'Inspection Booking',
        'listing': listing,
    })


def pay_placeholder(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'listings/coming_soon.html', {
        'feature': 'Rent Payment',
        'listing': listing,
    })