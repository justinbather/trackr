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
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect("dashboard")

    else:
        form = forms.CustomUserCreationForm()

    return render(request, "signup.html", {"form": form})


def login_user(request):
    user = request.user

    if request.POST:
        form = forms.UserForm(request.POST)
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "login.html", {"form": form})
    else:
        form = forms.UserForm()
        return render(request, "login.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect("../login")


def update_user(request):
    if request.user.is_authenticated:
        current_user = models.User.objects.get(id=request.user.id)
        form = forms.CustomUserCreationForm(request.POST or None, instance=current_user)
        return render(request, "profile.html", {"form": form})
    else:
        return redirect("../login")


def profile(request):
    if request.user.is_authenticated:
        current_user = models.User.objects.get(id=request.user.id)
        form = forms.UserProfileForm(request.POST or None, instance=current_user)
        return render(request, "profile.html", {"form": form})
    else:
        return redirect("../login")


def dashboard(request):
    user = request.user
    return render(request, "dashboard.html", {"first_name": user.first_name})


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
                return redirect("dashboard")
        return render(request, "create_team.html", {"form": form})
    return redirect("login")


def teams(request):
    if request.user.is_authenticated:
        user = models.User.objects.get(id=request.user.id)

        # Query DB for user owned teams to display
        owned_teams = models.Team.objects.filter(team_leader=user)

        # Query DB for user participating in team to display
        participating_teams = models.Team.objects.filter(teammember__member=user)

        context = {
            "participating_teams": participating_teams,
            "owned_teams": owned_teams,
        }

        return render(request, "teams.html", context)

    else:
        return redirect("login")


def team_dashboard(request, team_id):
    if request.user.is_authenticated:
        team = models.Team.objects.get(id=team_id)
        team_members = models.TeamMember.objects.filter(team=team)

        task_list = models.Task.objects.filter(team=team)
        team_score = models.Task.objects.filter(team=team, completed=True).count()
        try:
            team_goal = models.TeamGoal.objects.get(team=team)
            productivity = round(team_score / team_goal.goal * 100)
        except ObjectDoesNotExist:
            team_goal = "None"
            productivity = "A productivity score can only be calculated when a goal is created"
        team_score = models.Task.objects.filter(team=team, completed=True).count()
        

        # grabbing search form for user lookup and invite
        if "search" in request.GET:
            query = request.GET.get("search")
            # Prevents empty query from returning all users
            if query != "":
                user_search_results = models.User.objects.filter(email__contains=query)
                return render(
                    request,
                    "team_dashboard.html",
                    {
                        "team": team,
                        "user_search_results": user_search_results,
                        "user": request.user,
                        "team_members": team_members,
                    },
                )
        if request.POST:
            print(request.POST.get("id"))
            if "invite_user" in request.POST:
                invited_user = request.POST.get("id")
                print(invited_user)

        context = {
            "team": team, "user": request.user, 
            "team_members": team_members, 'task_list':task_list,
            'team_goal':team_goal, 'team_score':team_score, 'productivity':productivity
        }

        return render(
            request,
            "team_dashboard.html",
            context,
        )

    return redirect("login")


def invite_team_member(request, team_id, invited_user_id):
    if request.user.is_authenticated:
        team = models.Team.objects.get(id=team_id)
        invited_user = models.User.objects.get(id=invited_user_id)
        # will need error catching
        try:
            object = models.TeamMember.objects.get(team=team, member=invited_user)
            # return message that user is already in the team
            return redirect("team_dashboard", team_id)
        except ObjectDoesNotExist:
            models.TeamMember.objects.create(team=team, member=invited_user)
            return redirect("team_dashboard", team_id)
        # add success message here

    return redirect("login")


def all_owned_teams(request):
    if request.user.is_authenticated:
        user = models.User.objects.get(id=request.user.id)
        owned_teams = models.Team.objects.filter(team_leader=user)

        return render(request, "all_owned_teams.html", {"owned_teams": owned_teams})
    return redirect("login")
