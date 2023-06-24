from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='login', permanent=False)),
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_team/', views.create_team, name='create_team'),
    path('teams/', views.teams, name='teams'),
    path('teams/dashboard/<int:team_id>', views.team_dashboard, name='team_dashboard'),
    path('teams/dashboard/invite_member/<int:team_id>/<int:invited_user_id>', views.invite_team_member, name='invite_team_member'),
    path('teams/owned', views.all_owned_teams, name='all_owned_teams'),
    



    #path('update_user/', views.update_user, name='update_user'),
    #path('profile/', views.profile, name='profile'),
]