
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from . import models, forms
# Create your views here.


def signup(request):
    if request.method == "POST":
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('dashboard')

    else:
        form = forms.CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})


def login_user(request):
    user = request.user

    if request.POST:
        
        form = forms.UserForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = forms.UserForm()
        return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('../login')

def update_user(request):
    if request.user.is_authenticated:
        current_user = models.User.objects.get(id=request.user.id)
        form = forms.CustomUserCreationForm(request.POST or None, instance=current_user)
        return render(request, 'profile.html', {'form': form})
    else:
        return redirect('../login')

def profile(request):
    if request.user.is_authenticated:
        current_user = models.User.objects.get(id=request.user.id)
        form = forms.UserProfileForm(request.POST or None, instance=current_user)
        return render(request, 'profile.html', {'form': form})
    else:
        return redirect('../login')
    
def dashboard(request):
    user = request.user
    return render(request, 'dashboard.html', {'first_name':user.first_name})

def create_team(request):
    if request.user.is_authenticated:
        user = models.User.objects.get(id=request.user.id)
        form = forms.TeamCreationForm(request.POST)

        
        if request.POST:
            print(form.errors)
            if form.is_valid():
                form = form.save(commit=False)
                form.team_leader = user
                form.save()
                return redirect('dashboard')
        return render(request, 'create_team.html', {'form':form })
    return redirect('login')

def teams(request):
    if request.user.is_authenticated:
        user = models.User.objects.get(id=request.user.id)

        #Query DB for user owned teams to display
        owned_teams = models.Team.objects.filter(team_leader=user)
        
        #Query DB for user participating in team to display
        participating_teams = models.Team.objects.filter(member=user)

        
            
            
        context = {
            'participating_teams': participating_teams, 'owned_teams': owned_teams,
        }

        return render(request, 'teams.html', context)
    
    else:
        return redirect('login')
    

def team_dashboard(request, team_id):
    if request.user.is_authenticated:
        team = models.Team.objects.get(id=team_id)

        return render(request, "team_dashboard.html", {'team':team})
    
    return redirect('login')

def all_owned_teams(request):
    if request.user.is_authenticated:
        user = models.User.objects.get(id=request.user.id)
        owned_teams = models.Team.objects.filter(team_leader=user)

        return render(request, "all_owned_teams.html", {'owned_teams':owned_teams})
    return redirect('login')

        


                                                          






