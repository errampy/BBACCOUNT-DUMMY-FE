from django import forms
from .models import *
from django.forms import DateInput, DateTimeInput, TimeInput, CheckboxInput, Textarea, TextInput


class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    phone_number = forms.CharField(
        max_length=15, 
        required=True, 
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    roles = forms.CharField(
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    maker = forms.BooleanField(
        required=False, 
        widget=forms.CheckboxInput()
    )
    checker = forms.BooleanField(
        required=False, 
        widget=forms.CheckboxInput()
    )

    # You can also add validation or custom methods if needed

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError("A user with that email already exists.")
    #     return email
    

class LoginForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField()

class RoleForm(forms.Form):
    name = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
 