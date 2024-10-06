app_name = "CommRequests"

from django.urls import path
from .views import *

urlpatterns = [
    
    path('compose_request/', compose_request_view, name='compose_request'),
    path('request_pool/', request_pool_view, name="request_pool"),
    path('request_inbox', request_inbox_view, name="request_inbox"),
    path('request_outbox', request_outbox_view, name="request_outbox"),
    path('request_stats', request_stats_view, name="request_stats"),
    path('send_request', send_request_view, name = 'send_request'),
    path('compose_request_psp', compose_request_psp_view, name = 'compose_request_psp'),
    path('assign/<int:request_id>/', AssignRequestView.as_view(), name='assign_request'),
    path('request/<int:request_id>/', ciso_request_popup, name='ciso_request_popup'),
    path('request/<int:request_id>/', iso_request_popup, name='iso_request_popup'),
    path('request/<int:request_id>/', emp_request_popup, name='emp_request_popup'),


    #labs path
    path('addlab/', lab_add, name='addlab'),
    path('addlab/cisolabs/', cisolabs,), #displays all labs
    path('lab_details/<int:lab_id>', lab_details, name='lab_details'), #display lab details
    path('delete_employee/<int:lab_id>/',delete_members,name='delemp'), #display employee delete template
    path('delete_employee/<int:lab_id>/lab_details/',lab_details,name='lab_details'),
    path('add_employees/<int:lab_id>/',add_members, name='addemp' ),# display employee add template
    path('add_employees/<int:lab_id>/lab_details/',lab_details,name='lab_details'),
    path('add_head/<int:lab_id>/', edit_head, name = 'addhead'),
    path('add_head/<int:lab_id>/lab_details/',lab_details, name='lab_details'),
    path('lab/<int:lab_id>/projects/',lab_projects,name='project'), #display projects
    path('lab/<int:lab_id>/projects/add/',create_project,name='addproj'),
    path('lab/<int:lab_id>/projects/add/project/',lab_projects,name='project'),
    path('lab/<int:lab_id>/projects/<int:project_id>/edit/',edit_project,name='editproj'),
    path('lab/<int:lab_id>/projects/<int:project_id>/edit/project/',lab_projects,name='project'),
    path('cisolabs/', cisolabs ,name='cisolabs'),
    path('labs/delete/',delete_labs,name='delete_labs'),
    path('labs/delete/cisolabs/', cisolabs),
    
]