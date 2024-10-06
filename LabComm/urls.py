from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include(('CommRequests.urls','CommRequests'), namespace='CommRequests')),
    path('api/v1/getMeetSession', include('api.urls')),
    ]