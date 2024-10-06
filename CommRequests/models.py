from django.db import models
from django.contrib import admin
from main.models import User, Project
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
import os

def upload_file(instance, filename):
    ext = os.path.splitext(filename)[1]
    if ext.lower() in ['.pdf']:
        return f'pdfs/{filename}'
    else:
        return f'images/{filename}'

class Requests(models.Model):

    URGENCY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
        ('closed', 'Closed'),
    )

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipients = models.ManyToManyField(User, related_name='received_messages', limit_choices_to={'is_staff': False})
    subject = models.CharField(max_length=255)
    content = models.TextField(max_length=150,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null = True, blank = True)
    project_name = models.CharField(max_length=30, blank=False)
    domain_of_project = models.CharField(max_length=20, blank=False)
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, blank=False, default='low')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=False, default='open')
    deadline = models.DateField(null=True, blank=True)
    note = models.CharField(max_length = 100, null =True, blank = True)
    file = models.FileField(upload_to=upload_file, null=True, blank=True)


    def __str__(self):
        return self.subject
    
    def clean(self):
        super().clean()

        if self.recipients.count() > 3:
             raise ValidationError('You can only select up to three recipients.')

#LABS MODEL

class Labs(models.Model):
    DOMAIN_CHOICES = [
        ("CSec", "Cyber Security"),
        ("CComp", "Cloud Computing"),
        ("IT", "Information Technology"),
        ("SysArch", "System Architect")
    ]
    name = models.CharField(max_length=100, blank=False, null= False,unique=True )
    head = models.ForeignKey(User,on_delete=models.CASCADE,max_length=100, blank=False, null= False,related_name="lab_head")
    domain = models.CharField(max_length=15, blank=False, choices=DOMAIN_CHOICES, default='CSec')
    members= models.ManyToManyField(User,related_name='lab_members') 
    description=models.TextField()
    projects= models.ManyToManyField(Project,related_name='projects',blank=True, default=None) 
    
    
    def __str__(self):
        return self.name
    
#admin panel
class LabsAdmin(admin.ModelAdmin):
    
   
    list_display = ('name','head')
    search_fields =()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name=="head":
            User = get_user_model()
            kwargs['queryset']=User.objects.filter(designation="officer",is_active = True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name=="members":
            User = get_user_model()
            kwargs['queryset']=User.objects.filter(designation="employee", is_active = True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
