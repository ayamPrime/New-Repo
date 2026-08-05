from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django_ratelimit.decorators import ratelimit
from django.utils import timezone
from datetime import date
from .forms import PersonalInfoForm, AccountInfoForm, ContactInfoForm, ProfilePictureForm
from .models import CustomUser, UserProfile
from legal.models import LegalDocument

def signup_step1(request):
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST)
        if form.is_valid():
            # Store this step's data in the session.
            # dob is converted to a string because sessions only store
            # JSON-serialisable types — date objects aren't allowed.
            request.session['signup_step1'] = {
                'first_name': form.cleaned_data['first_name'],
                'last_name':  form.cleaned_data['last_name'],
                'dob':        form.cleaned_data['dob'].isoformat()
                              if form.cleaned_data['dob'] else None,
                'gender':     form.cleaned_data['gender'],
            }
            return redirect('signup_step2')
    else:
        form = PersonalInfoForm()
    return render(request, 'accounts/personal.html', {'form': form})

def signup_step2(request):
    # Guard: user cannot reach step 2 without completing step 1.
    # If the session key is missing they skipped — send them back.
    if 'signup_step1' not in request.session:
        return redirect('signup_step1')
 
    if request.method == 'POST':
        form = AccountInfoForm(request.POST)
        if form.is_valid():
            request.session['signup_step2'] = {
                'username':     form.cleaned_data['username'],
                'account_type': form.cleaned_data['account_type'],
                # Only store password1 — password2 was just for confirmation,
                # it's not needed after validation passes.
                'password':     form.cleaned_data['password1'],
            }
            return redirect('signup_step3')
    else:
        form = AccountInfoForm()
    return render(request, 'accounts/acct.html', {'form': form})

def signup_step3(request):
    if 'signup_step2' not in request.session:
        return redirect('signup_step1')
 
    if request.method == 'POST':
        form = ContactInfoForm(request.POST)
        if form.is_valid():
            request.session['signup_step3'] = {
                'email':        form.cleaned_data['email'],
                # PhoneNumber object → convert to string for session storage
                'phone_number': str(form.cleaned_data['phone_number']),
            }
            return redirect('signup_step4')
    else:
        form = ContactInfoForm()
    return render(request, 'accounts/contact.html', {'form': form})

def signup_step4(request):
    if 'signup_step3' not in request.session:
        return redirect('signup_step1')
 
    # Read account_type from the session to decide if image is required
    account_type = request.session.get('signup_step2', {}).get('account_type')
    is_lister = account_type == 'lister'
 
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
 
        # Enforce required image for listers at validation time
        if is_lister:
            form.fields['profile_image'].required = True
 
        if form.is_valid():
            # ── Pull all session data ──────────────────────────
            step1 = request.session.get('signup_step1', {})
            step2 = request.session.get('signup_step2', {})
            step3 = request.session.get('signup_step3', {})
 
            # Convert dob string back to a date object
            dob_str = step1.get('dob')
            dob = date.fromisoformat(dob_str) if dob_str else None
 
            # ── Create the user ────────────────────────────────
            # create_user() handles password hashing automatically.
            # Never use CustomUser.objects.create() for users —
            # that stores the plain password string directly.
            try:
                with transaction.atomic():
                    user = CustomUser.objects.create_user(
                        username =     step2['username'],
                        email =        step3['email'],
                        password =     step2['password'],
                        first_name =   step1['first_name'],
                        last_name =    step1['last_name'],
                        gender =       step1['gender'],
                        account_type = step2['account_type'],
                        phone_number = step3['phone_number'],
                        dob =          dob,
                    )
        
                    # ── Create UserProfile ─────────────────────────────
                    # Always created for every user — image may be empty.
                    # commit=False lets us attach the user before saving.
                    terms = LegalDocument.objects.get(doc_type="terms")
                    privacy = LegalDocument.objects.get(doc_type="privacy")
                    lister_onboarding = LegalDocument.objects.get(doc_type="lister_onboarding")
                    profile = form.save(commit=False)
                    profile.user = user
                    profile.agreed_to_terms = True
                    profile.agreed_to_terms_at = timezone.now()
                    profile.terms_version = terms.version
                    profile.agreed_to_privacy = True
                    profile.agreed_to_privacy_at = timezone.now()
                    profile.privacy_version = privacy.version
                    profile.agreed_to_lister_onboarding = True
                    profile.agreed_to_lister_onboarding_at = timezone.now()
                    profile.lister_onboarding_version = lister_onboarding.version
                    profile.save()
            except Exception as e:
                # If anything fails, the whole transaction rolls back.
                # Neither user nor profile ends up in the database.
                print(f"SIGNUP ERROR: {e}")
                form.add_error(None, f"Something went wrong. Please try again. {e}")
                return render(request, 'accounts/profile_image.html', {
                    'form':     form,
                    'is_lister': is_lister,
                })
 
            # ── Clean up session ───────────────────────────────
            for key in ['signup_step1', 'signup_step2', 'signup_step3']:
                try:
                    del request.session[key]
                except KeyError:
                    pass
 
            # ── Log the user in immediately ────────────────────
            # auth_login(request, user)
            # messages.success(request, f"Welcome to El Vanta, {user.first_name}!")
            return redirect('login')
 
    else:
        form = ProfilePictureForm()
        if is_lister:
            form.fields['profile_image'].required = True
 
    return render(request, 'accounts/profile_image.html', {
        'form':     form,
        'is_lister': is_lister,
    })

@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'Successfully logged in')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, 'Logout successful')
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        auth_logout(request)
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('home')
    return redirect('profile')