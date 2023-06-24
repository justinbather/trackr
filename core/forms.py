from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.forms import User
from django.utils.translation import gettext_lazy as _

from .models import User, Team

class CustomUserCreationForm(UserCreationForm):
    email = forms.CharField(max_length=100, required=True,
                            widget=forms.EmailInput
                            (attrs={'placeholder':'E-mail', 'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'}))
    first_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(attrs={ 'placeholder':'First Name', 'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'}))
    last_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput
                                (attrs={ 'placeholder':'Last Name', 'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'}))
    password1 = forms.CharField(max_length=30, required=True,
                                widget=forms.PasswordInput
                                (attrs={'placeholder':'Password', 'class': 'bg-gray-50 mb-10 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'}))
    password2 = forms.CharField(max_length=30, required=True,
                                widget=forms.PasswordInput
                                (attrs={'placeholder':'Verify Password', 'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'}))

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
                           (attrs={'class':"bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500", 'placeholder':'Email'}))
    password = forms.CharField(max_length=30,
                                widget=forms.PasswordInput
                                (attrs={'class':"bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500", 'placeholder':'Password'}))
    class Meta:
        model = User
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login')


class TeamCreationForm(ModelForm):
    team_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':"bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500", 'placeholder':'Team Name'}))
    team_leader = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(), required=False)


    class Meta:
        model = Team
        fields = ('team_name', 'team_leader')


