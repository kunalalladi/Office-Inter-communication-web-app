from django.apps import apps
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .models import *
from django.http import HttpResponseBadRequest
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from .forms import ImageUploadForm, add_achievement
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from datetime import date, datetime
import json
import secrets
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.core.exceptions import ValidationError
Labs =  apps.get_model('CommRequests', 'Labs')

class MyPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy("main:password_reset_complete")

class MyPasswordResetView(auth_views.PasswordResetView):
    email_template_name = 'registration/reset_password_email.html'
    success_url = reverse_lazy("main:password_reset_done")
    template_name = "registration/reset_password.html"

def employee_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_employee:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('main:unauthorized')

    return wrapper

def officer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_officer:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('main:unauthorized')

    return wrapper

def chiefofficer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_chiefofficer:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('main:unauthorized')

    return wrapper

def public_home_view(request):
    return render(request, "main/root.html")

@login_required
@employee_required
def employee_home_view(request):
    return render(request, "main/employee.html")

@login_required
@officer_required
def officer_home_view(request):
    return render(request, "main/officer.html")

@login_required
@chiefofficer_required
def chiefofficer_home_view(request):
    return render(request, "main/chief.html")

def normalize_username(username):
    return username.lower()

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        username = normalize_username(username)
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                if user.is_otp_req:  # Check if OTP is required for this user
                    send_otp(request, user)  # Send OTP only if is_otp_req is True
                    request.session["user_id"] = user.id
                    fname = user.first_name
                    return render(request, "registration/otp.html", {'fname': fname})
                else:
                    # If OTP is not required, log in the user directly without OTP
                    User.objects.get(username=user)
                    login(request, user)
                    if user.is_employee:
                        return redirect('main:employee_home')
                    elif user.is_officer:
                        return redirect('main:officer_home')
                    elif user.is_chiefofficer:
                        return redirect('main:chiefofficer_home')
            else:
                messages.error(request, 'Your account is not active. Please contact admin for verification.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    messages.success(request,"logged out Successfuly!")
    return redirect('/login')

def signup_view(request):
    domains = Domain.objects.all()
    if request.method == 'POST':
        try: 
            username=request.POST['username']
            first_name=request.POST['fname']
            last_name=request.POST['lname']
            user_email=request.POST['email']
            designation=request.POST.get('designation')
            domain=request.POST.get('domain')
            pass1=request.POST['pass1']
            pass2=request.POST['pass2']
            
            validate_password(pass1)

            if User.objects.filter(username=username):
                messages.error(request,"Username already Exist! please try some other Username")
                return redirect('/signup')

            if User.objects.filter(email=user_email):
                messages.error(request,'Email already registered! please try some other Email ')
                return redirect('/signup')
        

            if len(username)>20:
                messages.error(request,'Username must be under 10 characters')
                return redirect('/signup')
        
            if pass1 != pass2:
                messages.error(request,"Passwords didn't match!")
                return redirect('/signup')

            if not username.isalnum():
                messages.error(request,"Username must br Alpha-Numeric!")
                return redirect('/signup')
                
            user = User.objects.create_user(username, user_email, pass1)
            user.designation=designation
            user.domain= Domain.objects.get(name = domain)
            user.first_name = first_name
            user.last_name = last_name
            user.is_active=False
            user.is_verified = False
            user.save()
            primary_key = user.pk
            user.is_active=False
            user.is_verified = False
            if designation=="employee":
                user.is_employee = True
            elif designation=="officer":
                user.is_officer = True
            elif designation=="chief officer":
                user.is_chiefofficer = True
            
                
            #admin email
            admin_user= User.objects.get(is_superuser=True)
            admin_email = admin_user.email
                
            send_mail_after_registration(request, user, primary_key, admin_email, username, first_name, last_name, user_email, designation)
            user.save()
            return redirect('/token')
        except Exception and ValidationError as e:
            return render(request,'registration/signup.html',{'errors':e})

    else:

        return render(request, 'registration/signup.html', {'domains':domains})
    
    return render(request, 'registration/signup.html')

def send_mail_after_registration(request, user, primary_key, admin_email, username, first_name, last_name, user_email, designation):
    subject = "Welcome to project12"
    message = "Hello "+ first_name + "!! \n"+"Welcome to Project12 !! \nThankyou for visiting our website \nWe have also sent a confirmation email to admin, if he confirms it your account will be activated \n\n Thanking You\n Project12 Admin"
    from_email = settings.EMAIL_HOST_USER
    to_list= [user_email]
    send_mail(subject, message, from_email, to_list, fail_silently=True)


    #Email address Confirmation Email
    current_site = get_current_site(request)
    email_subject="confirm "+username+ "'s @project12 Login!!"
    message2=render_to_string('registration/email_confirmation.html',{
        'fname1': first_name,
        'lname1': last_name,
        'email1': user_email,
        'username1': username,
        'designation1': designation,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(primary_key)),
        'token':generate_token.make_token(user)
        })
    email=EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [admin_email],
        )
    email.fail_silently= True
    email.send()

def send_otp(request,user):
    generated_otp = str(secrets.randbelow(1000000)).zfill(6)
    subject="welcome to project12"
    message="welcome to project12\nyour Otp:"+str(generated_otp)+"\nplease do not share this otp with anyone!!\n\nThanking you\nLabComm Admin"
    request.session['value']=generated_otp
    from_email = settings.EMAIL_HOST_USER
    to_list= [user.email]
    request.session['otp_gen_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    send_mail(subject ,message, from_email, to_list, fail_silently=True)

def otp(request):
    if request.method == "POST":
        otp1=request.POST['otp']
        generated_otp=request.session['value']
        attempts = request.session.get('attempts', 0)
        if generated_otp==otp1:
            user_id = request.session.get('user_id')
            user = User.objects.get(id=user_id)
            if not user.is_superuser:
                login(request, user)
                del request.session['user_id']
                del request.session['value']
                request.session.pop('attempts', None)
                if user.is_employee:
                    return redirect('main:employee_home')
                elif user.is_officer:
                    return redirect('main:officer_home')
                elif user.is_chiefofficer:
                    return redirect('main:chiefofficer_home')
            else:
                messages.error(request,"Admins can only login to administrator site!")
                return redirect('/login')
        else:
            attempts += 1
            request.session['attempts'] = attempts
            if attempts >= 3:
                del request.session['user_id']
                del request.session['value']
                request.session.pop('attempts', None)
                messages.error(request,"Invalid OTP Entered 3 times. Try Again!")
                return redirect('/login')
            else:
                messages.error(request, "Incorrect OTP! You have " + str(3 - attempts) + " attempts remaining.")
                return redirect("main:otp")
    return render(request,"registration/otp.html")

def activate(request, uidb64, token):
    try:
        uid= force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user= None
    if user is not None and generate_token.check_token(user,token):
        user.is_active=True
        user.save()
        if user.is_active==True:
            subject = "Welcome to project12!"
            message = "Hello "+ user.first_name + "|| \n" + " your account has been verified by the admin.\nNow you can use the credentials to login."
            from_email = settings.EMAIL_HOST_USER
            to_list=[user.email]
            user.is_verified = True
            send_mail(subject, message, from_email, to_list, fail_silently=True)
        messages.success(request, 'The account has been verified!')
        return redirect('/success')
    
    elif user.is_active:
        messages.error(request, 'The account has already been verified!')
        return redirect('/success')

    else:
        
        messages.error(request, 'The verification link is invalid or has expired.')

        return redirect('registration/activation_failed.html')
    
def token_send(request):
    return render(request , 'registration/token_send.html')

def success(request):
    return render(request , 'registration/success.html')

def resend_otp(request):
        prev_otp_time_str = request.session.get('otp_gen_time')
        if prev_otp_time_str is not None:
            prev_otp_time = datetime.datetime.strptime(prev_otp_time_str, '%Y-%m-%d %H:%M:%S')
            elapsed_time = datetime.datetime.now() - prev_otp_time
            elapsed_seconds = elapsed_time.total_seconds()

            if elapsed_seconds < 60:
                messages.error(request,"Please wait for another "+str(int(60-elapsed_seconds))+" seconds to resend otp")
                return redirect ('main:otp')
            
            user_id = request.session.get('user_id')
            user = User.objects.get(id=user_id)
            
            send_otp(request, user)
            messages.success(request,"A new OTP has been sent to your Registered Email address!")

        return redirect('/otp')

def unauthorized_view(request):
    return render(request, "main/unauthorized.html")


def profile_view(request):
    user = request.user
    user_id = user.id
    today = date.today()
    date_of_joining = user.date_of_joining
    if date_of_joining:
        experience_years = today.year - date_of_joining.year
        if today.month < date_of_joining.month:
            experience_years -= 1
    else:
        experience_years = None    
    qualifications = user.qualifications if user.qualifications else None    
    achievements = Achievement.objects.filter(user=user)
    if user.designation == "employee":
        lab = Labs.objects.filter(members=user).values_list('name', flat=True)
    else :
        lab = Labs.objects.filter(head=user).values_list('name', flat=True)
    projects = Project.objects.filter(team_members=user)
    
    domain_choices_dict = dict(User.DOMAIN_CHOICES)
    
    project_details = []
    for project in projects:
        domain = domain_choices_dict.get(project.project_domain)
        project_details.append({
        'name': project.project_name,
        'completionDate': project.finished_at.strftime('%Y-%m-%d'),
        'domain': domain if domain else 'Unknown',
        })
    projects_json = json.dumps(project_details)

    context = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'user_id': user_id,
        'desg': user.designation,  
        'experience_years': experience_years,
        'qualifications': qualifications,
        'photo': user.photo.url, 
        'achievements': achievements,
        'lab':lab,
        'project_details': project_details,
        'projects_json' : projects_json,
        'request':request,

    }
    return render(request, 'main/profile/profile.html', context)

def editphoto_view(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            user_profile = get_object_or_404(User, id=request.user.id)
            user_profile.photo.delete()
            user_profile.photo.save(image_file.name, image_file)
            user_profile.save()
            return redirect('/profile')
        else:
            return HttpResponseBadRequest("No image file found.")
    else:
        return render(request, 'main/profile/profile.html')


def add_achievement_view(request):
    if request.method == 'POST':
        title1 = request.POST.get('title1')
        title2 = request.POST.get('title2')
        achievement1 = Achievement(user=request.user, title=title1)
        achievement1.save()
        achievement2 = Achievement(user=request.user, title=title2)
        achievement2.save()
        return redirect('/profile')
    else:
        return render(request, 'main/profile/profile.html')

def profilecard_view(request):
    current_user = request.user
    users = User.objects.exclude(Q(username=current_user.username) | Q(is_superuser=True))
    
    # Prepare user data
    user_list = []
    for user in users:
        # Calculate experience based on date of joining
        today = date.today()
        years_of_experience = None
        if user.date_of_joining:
            years_of_experience = today.year - user.date_of_joining.year
        user_data = {
            'photo': user.photo.url if user.photo else '',
            'fullName': user.get_full_name(),
            'designation': user.designation,
            'experience': years_of_experience,
            'domain': user.domain,
            'username' :user.username
        }
        user_list.append(user_data)

    # Serialize user data to JSON format
    users_json = json.dumps(user_list)

    context = {
        'users_json': users_json,
        'request':request,
        'chief_user':User.objects.filter(designation="chief officer", is_active =True),
    }


    return render(request, 'main/profile/profilecard.html',context)

@login_required
def delete_selected_users(request):
    if request.method == 'POST':
        user_ids = request.POST.getlist('selected_users[]')
        
        try:
            # Delete users with the selected user IDs from the database
            User.objects.filter(id__in=user_ids).delete()
            messages.success(request, 'Selected users have been deleted successfully.')
        except Exception as e:
            messages.error(request, f'Error occurred while deleting users: {str(e)}')

    return redirect('main:profilecard')

