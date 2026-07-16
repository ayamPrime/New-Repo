from django import forms
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.formfields import PhoneNumberField
from .models import CustomUser, UserProfile

class PersonalInfoForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label='Date of Birth'
    )
    gender = forms.ChoiceField(choices=CustomUser.Gender.choices)


class AccountInfoForm(forms.Form):
    username = forms.CharField(max_length=150)
    account_type = forms.ChoiceField(choices=CustomUser.AccType.choices)
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput
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
    email = forms.EmailField()
    phone_number = PhoneNumberField(region='NG')

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Not required — students can skip, agents are encouraged but not forced
        self.fields['profile_image'].required = False