from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.forms import User
from django.utils.translation import gettext_lazy as _

from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.CharField(max_length=100, required=True,
                            widget=forms.EmailInput
                            (attrs={'placeholder':'email'}))
    first_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(attrs={ 'placeholder':'first name'}))
    last_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput
                                (attrs={ 'placeholder':'last name'}))
    password1 = forms.CharField(max_length=30, required=True,
                                widget=forms.PasswordInput
                                (attrs={'placeholder':'password'}))
    password2 = forms.CharField(max_length=30, required=True,
                                widget=forms.PasswordInput
                                (attrs={'placeholder':'verify password'}))

    class Meta:
        model = User
        fields = ['first_name','last_name','email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = User
        fields = ('email','first_name', 'last_name')

class UserForm(forms.ModelForm):
    email= forms.CharField(max_length=100,
                           widget= forms.EmailInput
                           (attrs={'class':'username_input', 'placeholder':'Email'}))
    password = forms.CharField(max_length=30,
                                widget=forms.PasswordInput
                                (attrs={'class':'password_input', 'placeholder':'Password'}))
    class Meta:
        model = User
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login')