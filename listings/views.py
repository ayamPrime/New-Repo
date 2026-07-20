from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from .forms import ListingForm, LocationForm, AmenitiesForm, ListingImagesForm, ListingVideoForm, ListingFlagForm
from .models import Listing, ListingFlag, ListingImage

# Create your views here.
def home_page(request):
    listings = Listing.objects.order_by('-id')[:3]
    return render(request, 'listings/index.html', {'listings': listings})

def listings_page(request):
    listings = Listing.objects.all()
    query = request.GET.get('q', '').strip()
    if query:
        listings = listings.filter(property_type__icontains=slugify(query))
    return render(request, 'listings/listings.html', {'listings': listings, 'query': query})

@login_required
def add_listings(request):
    if request.user.account_type != 'lister':
        return redirect('home')

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        form1 = LocationForm(request.POST)
        form2 = AmenitiesForm(request.POST)
        images_form = ListingImagesForm(request.POST, request.FILES)
        form4 = ListingVideoForm(request.POST, request.FILES)

        forms_valid = [
            form.is_valid(),
            form1.is_valid(),
            form2.is_valid(),
            images_form.is_valid(),
            form4.is_valid(),
        ]

        if all(forms_valid):
            listing = form.save(commit=False)
            listing.lister = request.user
            listing.save()

            location = form1.save(commit=False)
            location.listing = listing
            location.save()

            amenities = form2.save(commit=False)
            amenities.listing = listing
            amenities.save()

            for img in images_form.cleaned_data['images']:
                ListingImage.objects.create(listing=listing, image=img)

            if request.FILES.get('video'):
                video = form4.save(commit=False)
                video.listing = listing
                video.save()

            return redirect('profile')
    else:
        form = ListingForm()
        form1 = LocationForm()
        form2 = AmenitiesForm()
        images_form = ListingImagesForm()
        form4 = ListingVideoForm()

    return render(request, 'listings/add_listings.html', {
        'listing_form': form,
        'location_form': form1,
        'amenities_form': form2,
        'images_form': images_form,
        'video_form': form4,
    })

def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'listings/listing_details.html', {'listing': listing})

@login_required
def flag_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    # Prevent flagging your own listing
    if request.user == listing.lister:
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