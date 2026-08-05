from django import forms
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.formfields import PhoneNumberField
from .models import CustomUser, UserProfile

class PersonalInfoForm(forms.Form):
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Adaeze'})
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Okafor'})
    )
    dob = forms.DateField(
        widget = forms.DateInput(attrs = {'type': 'date'}),
        required = False,
        label = 'Date of Birth'
    )
    gender = forms.ChoiceField(
        choices=CustomUser.Gender.choices,
        widget=forms.Select(attrs={'placeholder': 'Select your gender'})
    )


class AccountInfoForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. adaeze_o'})
    )
    account_type = forms.ChoiceField(
        choices=CustomUser.AccType.choices,
        widget=forms.RadioSelect
    )
    password1 = forms.CharField(
        label = 'Password',
        widget = forms.PasswordInput(attrs={'placeholder': 'Create a secure password'})
    )
    password2 = forms.CharField(
        label = 'Confirm Password',
        widget = forms.PasswordInput(attrs={'placeholder': 'Re-enter your password'})
    )

    def clean_username(self):
        # Checks DB for duplicate username at validation time
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_password1(self):
        # Runs Django's full AUTH_PASSWORD_VALIDATORS list
        # Same rules UserCreationForm uses — min length, common passwords, etc.
        password1 = self.cleaned_data.get('password1')
        if password1:
            validate_password(password1)
        return password1

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class ContactInfoForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'e.g. adaeze@example.com'})
    )
    phone_number = PhoneNumberField(
        region='NG',
        widget=forms.TextInput(attrs={'placeholder': '0XX XXXX XXXX'})
    )

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        return email

class ProfilePictureForm(forms.ModelForm):
    agree_to_terms = forms.BooleanField(
        required = True,
        error_messages = {'required': 'You must agree to the Terms of Service to create an account.'}
    )
    agree_to_privacy = forms.BooleanField(
        required=True,
        label = "I have read and accept the Privacy Policy",
        error_messages = {'required': 'You must agree to the Privacy Policy to create an account.'}
    )
    lister_onboarding_agreement = forms.BooleanField(
        required = True,
        label = "I have read and agree to the Lister Onboarding Agreement",
        error_messages = {'required': 'You must agree to the Lister Onboarding Agreement to create an account.'}
    )   
    class Meta:
        model = UserProfile
        fields = ['profile_image']
        widgets = {
            'profile_image': forms.ClearableFileInput(
                attrs={'accept': 'image/jpeg,image/png'}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Not required — students can skip, agents are encouraged but not forced
        self.fields['profile_image'].required = False