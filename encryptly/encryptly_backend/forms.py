from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.forms import CheckboxInput

from encryptly_backend.models import UserProfile, ContactRequest


class UserForm(forms.ModelForm):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Username"}), max_length=15)
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Password"}), max_length=100, min_length=10, )
    confirm_password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Confirm password", 'data-parsley-equalto': "#id_password"}), max_length=100, min_length=10)

    class Meta:
        model = User
        fields = ("username", "password")

    def clean(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if not confirm_password:
            raise forms.ValidationError("You must confirm your password")
        if password != confirm_password:
            raise forms.ValidationError("Your passwords do not match")

        return self.cleaned_data


class ProfileForm(forms.ModelForm):
    public_key = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "textbox-hidden", 'data-parsley-required': "false"}))
    private_key = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "textbox-hidden", 'data-parsley-required': "false"}))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    two_factor = forms.BooleanField(label="Enable two-factor authentication", widget=CheckboxInput(), required=False)
    mobile_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Mobile number"}), validators=[phone_regex], max_length=15, required=False)


    class Meta:
        model = UserProfile
        fields = ('public_key', 'private_key', 'two_factor', 'mobile_number')


class ContactForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control"}), max_length=3000)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder': "(optional)"}), required=False)

    class Meta:
        model = ContactRequest
        fields = ("message", "email")

    def clean(self):
        message = self.cleaned_data.get("message")

        if len(message) == 0:
            raise forms.ValidationError("No message specified!")

        return self.cleaned_data
