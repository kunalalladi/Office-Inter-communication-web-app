from django.urls import path
from . import views

urlpatterns = [
    path('', views.MySecureAPIView.as_view()),
]
