from typing import Dict, Optional
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Achievement, Project, Domain
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext as _
import re
# from django.apps import apps
from django import forms
from cryptography.fernet import Fernet


class UserAdminCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True)
    date_of_joining = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    qualifications = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'email', 'domain', 'designation', 'date_of_joining', 'qualifications', 'photo', 'is_active','is_employee', 'is_officer', 'is_chiefofficer', 'is_superuser')

    def clean(self):
        cleaned_data = super().clean()
        is_employee = cleaned_data.get('is_employee')
        is_officer = cleaned_data.get('is_officer')
        is_chiefofficer = cleaned_data.get('is_chiefofficer')
        is_superuser = cleaned_data.get('is_superuser')
        
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        num_selected = sum([is_employee, is_officer, is_chiefofficer, is_superuser])

        # If more than one option is selected, raise a validation error
        if num_selected > 1:
            raise forms.ValidationError("Only one option can be selected among is_employee, is_officer, is_chiefofficer, and is_superuser.")
        # Check if the password contains at least one capital letter
        if not any(char.isupper() for char in password):
            raise ValidationError(_("Password must contain at least one capital letter."))

        # Check if the password contains at least one number
        if not any(char.isdigit() for char in password):
            raise ValidationError(_("Password must contain at least one number."))

        # Check if the password contains at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(_("Password must contain at least one special character."))
        # Check password length
        if len(password) < 8:
            raise ValidationError(_("Password must be at least 8 characters long."))

        # Check if the password is related to any other field in the form
        for field_name, field_value in self.cleaned_data.items():
            if field_name != 'password' and field_name != 'confirm_password':
                if str(field_value) in password:
                    raise ValidationError(_("Password cannot contain related information with other fields."))

    
        if not password:
            raise forms.ValidationError("Please enter the password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data


    def save(self, commit=True):
        user = super().save(commit=False)

        # Set is_employee, is_officer, is_chiefofficer, is_superuser based on designation
        designation = self.cleaned_data.get('designation')
        if designation == 'employee':
            user.is_employee = True
            user.is_officer = False
            user.is_chiefofficer = False
            user.is_superuser = False
        elif designation == 'officer':
            user.is_employee = False
            user.is_officer = True
            user.is_chiefofficer = False
            user.is_superuser = False
        elif designation == 'chief officer':
            user.is_employee = False
            user.is_officer = False
            user.is_chiefofficer = True
            user.is_superuser = False
        elif designation == 'admin':
            user.is_employee = False
            user.is_officer = False
            user.is_chiefofficer = False
            user.is_superuser = True

        # Hash the password using Django's make_password method
        password = self.cleaned_data.get('password')
        user.password = make_password(password)

        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'email', 'domain', 'designation', 'date_of_joining', 'qualifications', 'photo','is_active',
                  'is_employee', 'is_officer', 'is_chiefofficer', 'is_superuser')
    
    def clean_password(self):
        # Check if the password field has been changed in the form
        if 'password' in self.changed_data:
            raise ValidationError("You cannot change the password from this form.")
        return self.cleaned_data['password']
    
    def save(self, commit=True):
        user = super().save(commit=False)

        # Check if the designation field has been changed in the form
        if 'designation' in self.changed_data:
            designation = self.cleaned_data.get('designation')
            if designation == 'employee':
                user.is_employee = True
                user.is_officer = False
                user.is_chiefofficer = False
                user.is_superuser = False
            elif designation == 'officer':
                user.is_employee = False
                user.is_officer = True
                user.is_chiefofficer = False
                user.is_superuser = False
            elif designation == 'chief officer':
                user.is_employee = False
                user.is_officer = False
                user.is_chiefofficer = True
                user.is_superuser = False
            elif designation == 'admin':
                user.is_employee = False
                user.is_officer = False
                user.is_chiefofficer = False
                user.is_superuser = True

        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        is_employee = cleaned_data.get('is_employee')
        is_officer = cleaned_data.get('is_officer')
        is_chiefofficer = cleaned_data.get('is_chiefofficer')
        is_superuser = cleaned_data.get('is_superuser')

        # Count how many options are selected
        num_selected = sum([is_employee, is_officer, is_chiefofficer, is_superuser])

        # If more than one option is selected, raise a validation error
        if num_selected > 1:
            raise forms.ValidationError("Only one option can be selected among is_employee, is_officer, is_chiefofficer, and is_superuser.")
        elif num_selected == 0:
            raise forms.ValidationError("Select one option among is_employee, is_officer, is_chiefofficer, and is_superuser.")


        return cleaned_data

class CustomUserAdmin(UserAdmin):
    add_form = UserAdminCreationForm
    form = UserAdminChangeForm
    list_display = ('username', 'email','first_name','last_name','domain','designation','is_superuser')
    list_filter =['is_superuser','domain','designation']
    fieldsets = (
        (None,{'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'domain', 'designation', 'date_of_joining', 'qualifications','photo')}),
        ('Privileges', {'fields': ('is_superuser','is_active','is_employee', 'is_officer', 'is_chiefofficer')}),
    )
    add_fieldsets = (
         ( None,{
              'classes': ('wide',),
              'fields': ('username','password','confirm_password','email','first_name','last_name','domain','designation', 'date_of_joining', 'qualifications','photo','is_active','is_employee','is_officer','is_chiefofficer','is_superuser'),}
          ),
      )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    # def save_model(self, request, obj, form, change):
    #     if 'password' in form:
    #         password = request.POST.get('password')
    #         confirm_password = request.POST.get('confirm_password')

    #         # Encrypt the password
    #         key = Fernet.generate_key()
    #         cipher_suite = Fernet(key)
    #         encrypted_password = cipher_suite.encrypt(password.encode()).decode()
    #         obj.password = encrypted_password

    #         # Encrypt the confirm password
    #         encrypted_confirm_password = cipher_suite.encrypt(confirm_password.encode()).decode()
    #         obj.confirm_password = encrypted_confirm_password

    #     super().save_model(request, obj, form, change)


    def get_fieldsets(self, request, obj= None ):
        fieldsets= super().get_fieldsets(request, obj)
        if not obj :
            fieldsets += (('Permissions',{'fields':('user_permissions',)}),) 
        if  obj :
            fieldsets += (('Permissions',{'fields':('user_permissions',)}),) 
        return fieldsets

    
    
class ProjectAdminForm(forms.ModelForm):
    team_members = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False
    )

    class Meta:
        model = Project
        fields = ('project_name', 'project_domain', 'finished_at', 'project_status', 'description', 'lab', 'team_members')

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['team_members'].queryset = User.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        lab = cleaned_data.get('lab')
        team_members = cleaned_data.get('team_members')
        if lab and team_members:
            lab_members = lab.members.all()
            if any(member not in lab_members for member in team_members):
                self.add_error('team_members', 'Please select team members from the lab members.')

class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = ['project_name', 'project_domain', 'finished_at', 'project_status']
    list_filter =['project_domain','project_status','lab']
    
    def get_fields(self, request,obj =None):
        if obj:
            return ('project_name','project_domain','finished_at','project_status','description','lab','team_members')
        else:
            return ('project_name','project_domain','finished_at','project_status','description','lab')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['team_members'].queryset = obj.lab.members.all()
        else:
            form.base_fields['team_members'].queryset = User.objects.none()
        return form

    def save_model(self, request, obj, form, change):
        obj.save()
        obj.team_members.set(form.cleaned_data['team_members'])
        if obj.lab:
            lab = obj.lab
            lab.projects.add(obj)
            lab.save()
        else:
            obj.save()


admin.site.register(User,CustomUserAdmin)
admin.site.register(Achievement)
admin.site.register(Project,ProjectAdmin)
admin.site.register(Domain)


  
