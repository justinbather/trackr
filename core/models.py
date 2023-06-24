from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.utils.translation import gettext_lazy as _


from .managers import CustomUserManager


# Create your models here.

class User(AbstractUser):

    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=30, unique=False)
    last_name = models.CharField(max_length=30, unique=False)
    is_admin = models.BooleanField(default=False)
    


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    



    
class Team(models.Model):

    team_name = models.CharField(max_length=20)
    team_leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_leader')
    productivity_goal = models.IntegerField(blank=True, null=True)
    productivity_score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.team_name
    

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.member.first_name


    
class Task(models.Model):

    #Importance Choices

    URGENT = 'Urgent'
    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'

    IMPORTANCE_CHOICES = [
        (URGENT, _('Urgent')),
        (HIGH, _('High')),
        (MEDIUM, _('Medium')),
        (LOW, _('Low')),
    ]


    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignee')
    due_date = models.DateField()
    importance = models.CharField(choices=IMPORTANCE_CHOICES, max_length=10)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description
    

        
        

    


