app_name = 'main'

from django.urls import path,include
from .views import *
from django.contrib.auth import views as auth_views
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path('', include('CommRequests.urls')),
    path('', public_home_view, name='default'),
    path('employee_home', employee_home_view, name='employee_home'),
    path('officer_home', officer_home_view, name="officer_home"),
    path('chiefofficer_home', chiefofficer_home_view, name="chiefofficer_home"),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup', signup_view, name='signup'),
    path('activate/<uidb64>/<token>',activate, name="activate"),
    path('token' , token_send , name="token_send"),
    path('success' , success , name='success'),
    path('resend_otp', resend_otp, name='resend_otp'),
    path('otp', otp, name='otp'),
    path('unauthorized', unauthorized_view, name="unauthorized"),

    path('reset_password/', MyPasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "registration/reset_password_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "registration/change_password_complete.html"), name="password_reset_complete"),
    path('profilecard/',profilecard_view,name='profilecard'),
    path('profile/', profile_view, name='profile'),
    path('editprofilephoto',editphoto_view,name='editprofilephoto'),
    path('addachievement',add_achievement_view,name='addachievement'),
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "registration/change_password_complete.html"), name="password_reset_complete"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 