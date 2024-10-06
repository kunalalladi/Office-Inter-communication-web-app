from typing import Optional
from django.db import models
from django.contrib.auth.models import AbstractUser

class Domain(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    
    confirm_password = models.CharField(max_length=30, null=False)
    DESGN_CHOICES =[
    ("employee", "Employee"),
    ("officer", "Officer"),
    ("chief officer", "Chief Officer"),
    ("admin","Admin"),
    ]
    
    designation = models.CharField(blank=False, null=True, max_length=15, choices=DESGN_CHOICES, default="employee")
    domain = models.ForeignKey(Domain, on_delete=models.SET_NULL, null=True)
    
    #is_active = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_chiefofficer = models.BooleanField(default = False)
    is_officer = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default=False)
    is_otp_req = models.BooleanField(default=True)
    
    date_of_joining = models.DateField(null=True)
    qualifications = models.TextField(null=True, blank=True)
    photo = models.ImageField(default='default_profile.jpg')


class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=100)

class Project(models.Model):

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('onhold', 'OnHold'),
        ('closed', 'Closed'),
    )

    project_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='PID')
    project_name = models.CharField(blank = False,null=False, max_length = 50)
    project_domain = models.ForeignKey(Domain, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateField(null = True, blank = True)
    project_status = models.CharField(max_length=15, blank=False, choices=STATUS_CHOICES, default='open')
    team_members = models.ManyToManyField(User)
    description=models.TextField(null=False, default="")
    lab=models.ForeignKey('CommRequests.Labs',on_delete=models.CASCADE,related_name='lab_projects')
    def __str__(self):
        return self.project_name
    

