from django.shortcuts import render, redirect,  get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .forms import RequestForm
from .models import Requests, Labs
from main.models import User, Project
from datetime import datetime

import json
# from cryptography.fernet import Fernet
# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
# from django.views.decorators.csrf import csrf_exempt
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from .models import Employee, Officer

#LABS

#Adding labs function
def lab_add(request):
    if request.method == "POST":
        name = request.POST.get("name")
        head_id = request.POST.get("head")
        members_ids= request.POST.getlist("members")
        project_ids= request.POST.getlist("projects")
        # Retrieve the head and members users
        head= User.objects.get(id=head_id)
        members=User.objects.filter(id__in = members_ids)
        projects=Project.objects.filter(project_id__in = project_ids)
        
        #create a new lab instance
        lab = Labs.objects.create(name=name, head=head)
        lab.save()
        lab.members.set(members)
        lab.projects.set(projects)
        
        
        return redirect('cisolabs/')
    else :
        return render(request, 'labs/addlab.html',{'users1': User.objects.filter(designation="officer", is_active=True) , 'users2' : User.objects.filter(designation="employee", is_active=True),'projects':Project.objects.all() })

#displaying lab details
def lab_details(request, lab_id):
    
    lab = get_object_or_404(Labs,id=lab_id)
    total= len(lab.members.all()) #lab members count
    #projects=Project.objects.filter(lab=lab)
    projects_total= len(lab.projects.all()) #len lab projects 
    
    return render(request, 'labs/emplab2.html', {'lab':lab, 'total':total ,'chief_user': User.objects.filter(designation="chief officer", is_active= True), 'projects_total':projects_total})

#displaying labs
def cisolabs(request):
    
    labs=Labs.objects.all()
    
    return render(request,'labs/cisolabs.html',{'labs':labs , 'chief_user': User.objects.filter(designation="chief officer", is_active = True) , 'request':request })

#deleting lab members
def delete_members(request,lab_id):
    if request.method=='POST':
        selected_employees = request.POST.getlist('selected_employees')
        lab = get_object_or_404(Labs,id=lab_id)
        lab.members.remove(*selected_employees)
        lab_id= lab.id
        return redirect('lab_details/', lab_id=lab_id)
    else:
        lab = get_object_or_404(Labs,id=lab_id)
        lab_members=lab.members.all()
        return render(request, 'labs/delemp.html',{'lab_members':lab_members})
 
 
#adding employees to lab
def add_members(request,lab_id):
    if request.method=='POST':
        selected_employees_ids = request.POST.getlist('selected_employees') 
        lab = get_object_or_404(Labs,id=lab_id)
        selected_employees= User.objects.filter(id__in = selected_employees_ids)
        lab.members.add(*selected_employees)
        lab_id = lab.id 
        return redirect('lab_details/', lab_id=lab_id)
    else:
        lab = get_object_or_404(Labs,id=lab_id)
        employees= User.objects.filter(designation='employee', is_active = True)
        
        return render(request, 'labs/addemp.html',{'employees':employees})
#changing the head of lab
def edit_head(request, lab_id):
    if request.method=='POST':
        lab_head_id = request.POST.get('lab_head')
        lab = get_object_or_404(Labs,id=lab_id)
        previous_lab_head_id = lab.head.id
        
        if previous_lab_head_id:
            Labs.objects.filter(id=previous_lab_head_id).delete()
            
            
        new_lab_head = User.objects.get(id=lab_head_id)
        lab.head= new_lab_head
        lab.save()
        lab_id = lab.id 
        return redirect('lab_details/', lab_id=lab_id)
    else:
        lab = get_object_or_404(Labs,id=lab_id)
        officers = User.objects.filter(designation='officer', is_active = True)
        
        return render(request, 'labs/addhead.html',{'officers':officers})
        
#deleting multiple labs
def delete_labs(request):
    if request.method =='POST':
        selected_labs = request.POST.getlist('selected_labs')
        Labs.objects.filter(id__in=selected_labs).delete()
        return redirect('cisolabs/')
    else:
        labs=Labs.objects.all()
        return render(request, 'labs/delete.html',{'labs':labs})
    
#displaying lab project
def lab_projects(request,lab_id,*args,**kwargs):
    lab=get_object_or_404(Labs,id=lab_id)
    projects=lab.projects.all()
    
    
    for project in projects:
        team_members=json.dumps(list(project.team_members.all().values_list('username',flat=True)))
       
    context={
        'lab':lab,
        'projects':projects,
        'chief_user': User.objects.filter(designation="chief officer", is_active=True),
        'team_members':team_members,
    }
    return render(request, 'labs/project.html',context)

def create_project(request,lab_id):
    lab=get_object_or_404(Labs, id=lab_id)
    
    if request.method=='POST':
        
        project_name=request.POST.get('project_name')
        project_domain=request.POST.get('project_domain')
        finished_at=request.POST.get('finished_at')   
        project_status=request.POST.get('project_status')
        team_members_ids=request.POST.getlist("team_members")
        description=request.POST.get('description')
       
        project=Project.objects.create(
            
            project_name=project_name,
            project_domain=project_domain,
            finished_at=finished_at,
            project_status=project_status,
            description=description,
           
            )
        for member_id in team_members_ids:
            member=get_object_or_404(User,id=member_id)
            project.team_members.add(member)
        project.save()
        
        return redirect('project/',lab_id=lab.id)
    
    
        
    # Project.project_members.set(team_members)
    # projects=Labs.project_set.all()
    lab_members=lab.members.all()
    
    context={
        'lab':lab,
        
        'lab_members':lab_members,
    }
   
    return render(request,'labs/addproj.html',context)


def edit_project(request,lab_id,project_id):
    lab=get_object_or_404(Labs, id=lab_id)
    project=get_object_or_404(Project, project_id=project_id)
    if request.method=="POST":
        project.project_name=request.POST.get('project_name')
        project.project_domain=request.POST.get('project_domain')
        project.finished_at=request.POST.get('finished_at')
        project.project_status=request.POST.get('project_status')
        team_members_ids=request.POST.getlist("team_members") # the list of team members ids from the template
        project.description=request.POST.get('description')
        
        #update the projects team members
        project.team_members.clear() #clear the existing team members
        
        for member_id in team_members_ids:
            project.team_members.add(member_id)
            
        project.save()
        messages.success(request,"Successfully updated!")
        
        return redirect('project/',lab_id=lab.id)
    else:
        lab_members=lab.members.all()
        return render(request,'labs/editproj.html',{'lab':lab,'project':project,'lab_members':lab_members})
        
#chat

# # Generate a secret key for encryption
# secret_key = Fernet.generate_key()
# cipher_suite = Fernet(secret_key)

# # Dictionary to store active chat rooms
# active_chat_rooms = {}

# @csrf_exempt
# def start_chat(request):
#     # Parse the request data
#     data = json.loads(request.body)
#     employee_id = data.get('employee_id')
#     officer_id = data.get('officer_id')

#     # Retrieve the employee and officer objects
#     employee = get_object_or_404(Employee, id=employee_id)
#     officer = get_object_or_404(Officer, id=officer_id)

#     # Create a unique chat room ID
#     chat_room_id = f'chat_{employee_id}_{officer_id}'

#     # Generate encryption keys for the chat room
#     chat_room_key = Fernet.generate_key()
#     encrypted_chat_room_key = cipher_suite.encrypt(chat_room_key)

#     # Store the chat room details in the active_chat_rooms dictionary
#     active_chat_rooms[chat_room_id] = {
#         'employee': employee_id,
#         'officer': officer_id,
#         'key': chat_room_key
#     }

#     # Send the encrypted chat room key to both employee and officer
#     employee_channel = f'employee_{employee_id}'
#     officer_channel = f'officer_{officer_id}'

#     # Send encrypted chat room key to employee
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.send)(employee_channel, {
#         'type': 'send_chat_room_key',
#         'encrypted_chat_room_key': encrypted_chat_room_key,
#         'chat_room_id': chat_room_id,
#     })

#     # Send encrypted chat room key to officer
#     async_to_sync(channel_layer.send)(officer_channel, {
#         'type': 'send_chat_room_key',
#         'encrypted_chat_room_key': encrypted_chat_room_key,
#         'chat_room_id': chat_room_id,
#     })

#     return JsonResponse({'success': True, 'chat_room_id': chat_room_id})


# def decrypt_message(encrypted_message, key):
#     f = Fernet(key)
#     decrypted_message = f.decrypt(encrypted_message)
#     return decrypted_message.decode()


# def encrypt_message(message, key):
#     f = Fernet(key)
#     encrypted_message = f.encrypt(message.encode())
#     return encrypted_message


# @csrf_exempt
# def receive_message(request):
#     # Parse the request data
#     data = json.loads(request.body)
#     chat_room_id = data.get('chat_room_id')
#     sender = data.get('sender')
#     encrypted_message = data.get('encrypted_message')

#     # Retrieve the chat room details
#     chat_room = active_chat_rooms.get(chat_room_id)
#     if not chat_room:
#         return JsonResponse({'success': False, 'error': 'Invalid chat room'})

#     # Get the encryption key for the chat room
#     chat_room_key = chat_room['key']

#     # Decrypt the message
#     decrypted_message = decrypt_message(encrypted_message, chat_room_key)

#     # Send the decrypted message to the other participant
#     receiver = chat_room['employee'] if sender == 'officer' else chat_room['officer']
#     channel_name = f'officer_{receiver

# }' if sender == 'officer' else f'employee_{receiver}'

#     # Send the decrypted message to the receiver
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.send)(channel_name, {
#         'type': 'send_message',
#         'message': decrypted_message,
#         'sender': sender,
#     })

#     return JsonResponse({'success': True})


# @csrf_exempt
# def send_message(request):
#     # Parse the request data
#     data = json.loads(request.body)
#     chat_room_id = data.get('chat_room_id')
#     sender = data.get('sender')
#     message = data.get('message')

#     # Retrieve the chat room details
#     chat_room = active_chat_rooms.get(chat_room_id)
#     if not chat_room:
#         return JsonResponse({'success': False, 'error': 'Invalid chat room'})

#     # Get the encryption key for the chat room
#     chat_room_key = chat_room['key']

#     # Encrypt the message
#     encrypted_message = encrypt_message(message, chat_room_key)

#     # Send the encrypted message to the other participant
#     receiver = chat_room['employee'] if sender == 'officer' else chat_room['officer']
#     channel_name = f'officer_{receiver}' if sender == 'officer' else f'employee_{receiver}'

#     # Send the encrypted message to the receiver
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.send)(channel_name, {
#         'type': 'send_message',
#         'encrypted_message': encrypted_message,
#         'sender': sender,
#     })

#     return JsonResponse({'success': True})




        
   
    

from django.shortcuts import render, redirect,  get_object_or_404, HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import Requests, Labs
from main.models import User, Project, Domain
from django.core import serializers
from django.core.serializers import serialize
from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
import os
import json
from django.http import JsonResponse

def handle_uploaded_file(file):
    directory = 'request_files'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the file to the directory
    file_path = os.path.join(directory, file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_path



    
def compose_request_view(request):
    current_user = request.user
    if current_user.designation == "employee":
        officers = User.objects.filter(designation='officer')
    else:
        officers = User.objects.filter(designation='officer').exclude(username=current_user.username)
    domains = Domain.objects.all()
    projects = Project.objects.all()
    if request.method == 'POST':
        sender = request.user
        project_name = request.POST.get('project-name')
        domain = request.POST.get('domain')
        urgency = request.POST.get('urgency')
        deadline = request.POST.get('project-deadline')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        recipients = request.POST.get('recipient')

        files = request.FILES.getlist('file-upload')

        username = recipients
        user_email = User.objects.get(username=recipients).email
        first_name = User.objects.get(username=recipients).first_name
        sender_username = request.user.username
        sender_designation = request.user.designation

        file_paths = []  # List to store file paths for multiple uploaded files

        for file in files:
            file_path = handle_uploaded_file(file)
            file_paths.append(file_path)  # Append each file path to the list

        new_request = Requests(
                sender=sender,
                project_name=project_name,
                domain_of_project=domain,
                urgency=urgency,
                deadline=deadline,
                subject=subject,
                content=description,
                file=",".join(file_paths),  # Join file paths into a comma-separated string
        )
        new_request.save()
        new_request.recipients.set([recipients])
        send_mail_after_request(request, username, first_name, user_email, sender_username, sender_designation)

        messages.success(request,"The request has been sent successfully!")

        return render(request, 'request/compose_requests.html')
    else:
        return render(request, 'requests/compose_requests.html', {'officers': officers, 'domains': domains,'projects':projects})


def ciso_request_popup(request, request_id):
    # Assuming you have a URL pattern to capture the 'request_id'
    # in the URL, pass it to this view function.

    # Retrieve the request instance using the 'request_id'
    request_instance = get_object_or_404(Requests, id=request_id)

    # Handle POST request to accept or reject the request
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            # Perform the necessary action to accept the request
            # For example, you could update the 'status' field to 'in_progress'
            request_instance.status = 'in_progress'
            request_instance.save()
            return JsonResponse({'status': 'accepted'})
        elif action == 'reject':
            # Perform the necessary action to reject the request
            # For example, you could update the 'status' field to 'rejected'
            request_instance.status = 'rejected'
            request_instance.save()
            return JsonResponse({'status': 'rejected'})
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

    # For GET requests, render the template with the request details
    return render(request, 'requests/ciso_req_fin.html', {'request_instance': request_instance})

def iso_request_popup(request, request_id):
    # Assuming you have a URL pattern to capture the 'request_id'
    # in the URL, pass it to this view function.

    # Retrieve the request instance using the 'request_id'
    request_instance = get_object_or_404(Requests, id=request_id)

    # Handle POST request to accept or reject the request
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            # Perform the necessary action to accept the request
            # For example, you could update the 'status' field to 'in_progress'
            request_instance.status = 'in_progress'
            request_instance.save()
            return JsonResponse({'status': 'accepted'})
        elif action == 'reject':
            # Perform the necessary action to reject the request
            # For example, you could update the 'status' field to 'rejected'
            request_instance.status = 'rejected'
            request_instance.save()
            return JsonResponse({'status': 'rejected'})
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

    # For GET requests, render the template with the request details
    return render(request, 'requests/iso_req_fin.html', {'request_instance': request_instance})

def emp_request_popup(request, request_id):
    # Assuming you have a URL pattern to capture the 'request_id'
    # in the URL, pass it to this view function.

    # Retrieve the request instance using the 'request_id'
    request_instance = get_object_or_404(Requests, id=request_id)

    # Handle POST request to accept or reject the request
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            # Perform the necessary action to accept the request
            # For example, you could update the 'status' field to 'in_progress'
            request_instance.status = 'in_progress'
            request_instance.save()
            return JsonResponse({'status': 'accepted'})
        elif action == 'reject':
            # Perform the necessary action to reject the request
            # For example, you could update the 'status' field to 'rejected'
            request_instance.status = 'rejected'
            request_instance.save()
            return JsonResponse({'status': 'rejected'})
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

    # For GET requests, render the template with the request details
    return render(request, 'requests/employee_req_fin.html', {'request_instance': request_instance})

def send_request_view(request):
    domains = Domain.objects.all()
    projects = Project.objects.all()
    if request.method == 'POST':
        # Retrieve the username from the request's POST data
        recipient_username = request.POST.get('recipient', None)
        context = {
            'recipient_username' : recipient_username,
            'domains': domains,
            'projects':projects,
            
        }
        # Process the request and send the response (you can customize this part)
        if recipient_username:
            return render(request, 'requests/compose_requests_psp.html',context)
        else:
            return HttpResponse(f'Recipient username not provided')

    return HttpResponse(f'Invalid request method') 

def send_mail_after_request(request, username, first_name, user_email, sender_username, sender_designation):
    subject = username + " you've got a new request!!"
    message = "Hello "+ first_name + "!! \n"+sender_username+" has sent you a new request!! Kindly please login to check the request\n\ndesignation:"+sender_designation
    from_email = settings.EMAIL_HOST_USER
    to_list= [user_email]
    send_mail(subject, message, from_email, to_list, fail_silently=True)

def compose_request_psp_view(request):
    officers = User.objects.filter(designation='officer')
    domains = User.DOMAIN_CHOICES

    if request.method == 'POST':
        sender = request.user
        project_name = request.POST.get('project-name')
        domain = request.POST.get('domain')
        urgency = request.POST.get('urgency')
        deadline = request.POST.get('project-deadline')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        recipient = request.POST.get('recipient')

        files = request.FILES.getlist('file-upload')
        recipient_user = User.objects.get(username=recipient)

        user_email = User.objects.get(username=recipient).email
        first_name = User.objects.get(username=recipient).first_name
        sender_username = request.user.username
        sender_designation = request.user.designation

        file_paths = []  # List to store file paths for multiple uploaded files

        for file in files:
            file_path = handle_uploaded_file(file)
            file_paths.append(file_path)  # Append each file path to the list

        new_request = Requests(
                sender=sender,
                project_name=project_name,
                domain_of_project=domain,
                urgency=urgency,
                deadline=deadline,
                subject=subject,
                content=description,
                file=",".join(file_paths),  # Join file paths into a comma-separated string
        )
        new_request.save()
        new_request.recipients.set([recipient_user])
        send_mail_after_request(request, recipient , first_name, user_email, sender_username, sender_designation)

        return HttpResponse('Request submitted successfully!')
    else:
        return render(request, 'requests/compose_requests_psp.html', {'officers': officers, 'domains': domains})


def request_pool_view(request):

    fifteen_days_ago = timezone.now() - timedelta(days=15)
    requests = Requests.objects.filter(created_at__lt=fifteen_days_ago)
    request_json = serialize('json',requests,fields=('domain_of_project','urgency', 'status', 'project_name','created_at'))

    return render(request, 'requests/common_pool_req_fin.html', {'requests': request_json})

def request_inbox_view(request):

    fifteen_days_ago = timezone.now() - timezone.timedelta(days=15)

    # Get all the Requests objects that are less than 15 days old
    requests = Requests.objects.filter(created_at__gte=fifteen_days_ago)
    request_json = serialize('json',requests,fields=('domain_of_project','urgency', 'status', 'project_name','created_at'))

    return render(request, "requests/request_in.html", {"requests":request_json})

def request_outbox_view(request):
    requests = Requests.objects.filter(sender = request.user.id)
    request_json = serialize('json',requests,fields=('domain_of_project','urgency', 'status', 'project_name','created_at'))
    return render(request, "requests/request_out.html", {"requests":request_json})
    
def request_stats_view(request):
    
    requests_completed = Requests.objects.filter(status = 'completed', sender = request.user)
    requests_pending = Requests.objects.filter(
    Q(status='open') | Q(status='in_progress'),
    sender= request.user
)
    requests_sent = Requests.objects.filter(sender = request.user)
    requests_accepted = Requests.objects.filter(status = "completed", sender = request.user)
    requests_sent_count = requests_sent.count()
    requests_pending_count = requests_pending.count()
    requests_accepted_count = requests_accepted.count()
    requests_completed_count = requests_completed.count()
    requests = Requests.objects.filter(Q(sender = request.user) | Q(recipients = request.user))

    context = {
        'sent_count':requests_sent_count,
        'pending_count':requests_pending_count,
        'accepted_count':requests_accepted_count,
        'completed_count':requests_completed_count,
        'requests':requests,
    }

    return render(request, "requests/req_stats.html", context)

import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Requests
from .forms import AssignRequestForm

class AssignRequestView(View):
    template_name = 'requests/iso_req_fin.html'

    def get(self, request, request_id):
        request_instance = get_object_or_404(Requests, id=request_id)
        form = AssignRequestForm()
        return render(request, self.template_name, {'form': form, 'request_instance': request_instance})

    def post(self, request, request_id):
        request_instance = get_object_or_404(Requests, id=request_id)
        form = AssignRequestForm(request.POST)
        if form.is_valid():
            recipients = form.cleaned_data['recipients']
            request_instance.recipients.set(recipients)
            return redirect('request_detail', request_id=request_id)
        return render(request, self.template_name, {'form': form, 'request_instance': request_instance})

def request_inbox_view(request):
    if not request.user.is_authenticated:
        return redirect('main:login')

    requests = Requests.objects.filter(recipients=request.user, status = 'open')
    
    if request.user.designation == "employee":
        requests_json = serialize_requests(requests)
        return render(request, "requests/employee_req_fin.html", {"requests": requests_json,'request':request})
    elif request.user.designation == "officer":
        requests_json = serialize_requests(requests)
        return render(request, "requests/iso_req_fin.html", {"requests": requests_json,'request':request})
    else:
        requests_json = serialize_requests(requests)
        return render(request, "requests/ciso_req_fin.html", {"requests": requests_json,'request':request})

def serialize_requests(requests):
    # Convert the QuerySet of Requests objects to a list of dictionaries
    data = [
        {
            "fields": {
                "project_name": req.project_name,
                "domain_of_project": req.domain_of_project,
                "status": req.status,
                "created_at": req.created_at.strftime("%Y-%m-%d"),
                "urgency": req.urgency,
            }
        }
        for req in requests
    ]
    return json.dumps(data)  # Convert the list of dictionaries to a JSON string



#LABS

#Adding labs function
def lab_add(request):
    if request.method == "POST":
        name = request.POST.get("name")
        head_id = request.POST.get("head")
        domain=request.POST.get('domain')
        members_ids= request.POST.getlist("members")
        project_ids= request.POST.getlist("projects")
        # Retrieve the head and members users
        head= User.objects.get(id=head_id)
        members=User.objects.filter(id__in = members_ids)
        projects=Project.objects.filter(project_id__in = project_ids)
        
        #create a new lab instance
        lab = Labs.objects.create(name=name, head=head)
        lab.domain = domain
        lab.save()
       
        lab.members.set(members)
        lab.projects.set(projects)
        
        
        return redirect('cisolabs/')
    else :
        return render(request, 'labs/addlab.html',{'users1': User.objects.filter(designation="officer", is_active=True) , 'users2' : User.objects.filter(designation="employee", is_active=True),'projects':Project.objects.all() })

#displaying lab details
def lab_details(request, lab_id):
    
    lab = get_object_or_404(Labs,id=lab_id)
    total= len(lab.members.all()) #lab members count
    #projects=Project.objects.filter(lab=lab)
    projects_total= len(lab.projects.all()) #len lab projects 
    context={
        'lab':lab, 
        'total':total,
        'chief_user': User.objects.filter(designation="chief officer", is_active= True),
        'projects_total':projects_total,
        'request':request,
    }
    
    return render(request, 'labs/emplab2.html', context)

#displaying labs
def cisolabs(request):
    labs = Labs.objects.all()
    labs_json = serializers.serialize('json', labs)

    lab_members_count = {}
    lab_head_usernames = {}

    for lab in labs:
        lab_members_count[lab.id] = lab.members.count()
        if lab.head:
            lab_head_usernames[lab.id] = lab.head.username

    context = {
        'labs_json': labs_json,
        'lab_members_count': lab_members_count,
        'lab_head_usernames': lab_head_usernames,
        'request':request,
        'chief_user': User.objects.filter(designation="chief officer", is_active= True),
        
    }

    return render(request, 'labs/cisolabs.html', context)


#deleting lab members
def delete_members(request,lab_id):
    if request.method=='POST':
        selected_employees = request.POST.getlist('selected_employees')
        lab = get_object_or_404(Labs,id=lab_id)
        lab.members.remove(*selected_employees)
        lab_id= lab.id
        return redirect('lab_details/', lab_id=lab_id)
    else:
        lab = get_object_or_404(Labs,id=lab_id)
        lab_members=lab.members.all()
        return render(request, 'labs/delemp.html',{'lab_members':lab_members})
 
 
#adding employees to lab
def add_members(request,lab_id):
    if request.method=='POST':
        selected_employees_ids = request.POST.getlist('selected_employees') 
        lab = get_object_or_404(Labs,id=lab_id)
        selected_employees= User.objects.filter(id__in = selected_employees_ids)
        lab.members.add(*selected_employees)
        lab_id = lab.id 
        return redirect('lab_details/', lab_id=lab_id)
    else:
        lab = get_object_or_404(Labs,id=lab_id)
        employees= User.objects.filter(designation='employee', is_active = True)
        
        return render(request, 'labs/addemp.html',{'employees':employees})
#changing the head of lab
def edit_head(request, lab_id):
    if request.method=='POST':
        lab_head_id = request.POST.get('lab_head')
        lab = get_object_or_404(Labs,id=lab_id)
        previous_lab_head_id = lab.head.id
        
        if previous_lab_head_id:
            Labs.objects.filter(id=previous_lab_head_id).delete()
            
            
        new_lab_head = User.objects.get(id=lab_head_id)
        lab.head= new_lab_head
        lab.save()
        lab_id = lab.id 
        chief_user: User.objects.filter(designation="chief officer", is_active=True)
        
        return redirect('lab_details/', lab_id=lab_id,)
    else:
        lab = get_object_or_404(Labs,id=lab_id)
        officers = User.objects.filter(designation='officer', is_active = True)
        
        return render(request, 'labs/addhead.html',{'officers':officers})
        
#deleting multiple labs
def delete_labs(request):
    if request.method =='POST':
        selected_labs = request.POST.getlist('selected_labs')
        Labs.objects.filter(id__in=selected_labs).delete()
        return redirect('cisolabs/')
    else:
        labs=Labs.objects.all()
        return render(request, 'labs/delete.html',{'labs':labs})
    
#displaying lab project
def lab_projects(request,lab_id,*args,**kwargs):
    lab=get_object_or_404(Labs,id=lab_id)
    projects=lab.projects.all()
    
    l1 = len(lab.projects.all())
    for project in projects:
        team_members=list(project.team_members.all().values_list('username',flat=True)) 
        
    if l1!=0:
        context={
            'lab':lab,
            'projects':projects,
            'chief_user': User.objects.filter(designation="chief officer", is_active=True),
            'team_members':json.dumps(team_members),
        }
    else:
        context={
            'lab':lab,
            'projects':projects,
            'chief_user': User.objects.filter(designation="chief officer", is_active=True),}
    
    return render(request, 'labs/project.html',context)

def create_project(request,lab_id):
    lab=get_object_or_404(Labs, id=lab_id)
    
    if request.method=='POST':
        
        project_name=request.POST.get('project_name')
        project_domain=request.POST.get('project_domain')
        finished_at=request.POST.get('finished_at')   
        project_status=request.POST.get('project_status')
        team_members_ids=request.POST.getlist("team_members")
        description=request.POST.get('description')
       
        project=Project.objects.create(
            
            project_name=project_name,
            project_domain=project_domain,
            finished_at=finished_at,
            project_status=project_status,
            description=description,
            lab = lab,
            )
        for member_id in team_members_ids:
            member=get_object_or_404(User,id=member_id)
            project.team_members.add(member)
        project.save()
        lab.projects.add(project)
        lab.save()
        return redirect('project/',lab_id=lab.id)
    
    lab_members=lab.members.all()
    
    context={
        'lab':lab,
        
        'lab_members':lab_members,
    }
   
    return render(request,'labs/addproj.html',context)


def edit_project(request,lab_id,project_id):
    lab=get_object_or_404(Labs, id=lab_id)
    project=get_object_or_404(Project, project_id=project_id)
    if request.method=="POST":
        project.project_name=request.POST.get('project_name')
        project.project_domain=request.POST.get('project_domain')
        project.finished_at=request.POST.get('finished_at')
        project.project_status=request.POST.get('project_status')
        team_members_ids=request.POST.getlist("team_members") # the list of team members ids from the template
        project.description=request.POST.get('description')
        
        #update the projects team members
        project.team_members.clear() #clear the existing team members
        
        for member_id in team_members_ids:
            member = get_object_or_404(User, id=member_id)
            project.team_members.add(member)
            
        project.save()
        messages.success(request,"Successfully updated!")
        
        return redirect('project/',lab_id=lab.id)
    else:
        lab_members=lab.members.all()
        return render(request,'labs/editproj.html',{'lab':lab,'project':project,'lab_members':lab_members})

        