from django.urls import path,include
from .views import *
from django.contrib.auth import views as auth_views

from django.conf.urls import url
urlpatterns = [
    path('', profile, name='profile'),
    path('register/',register,name="register"),
    path('login/',auth_views.LoginView.as_view(template_name='students/login.html'),name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='students/logout.html'),name = 'logout'),
    path('update/',updateStudent,name='update-student'),
    path('save/',saveStudents,name='save-student'),
    path('updatesubjects/',updateSubjects,name='update-subjects'),
    path('saveandupdate/',saveandupdate,name='save-update'),
    path('setprofile/',setprofile,name='set-profile'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='students/password_reset.html'),name = 'password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='students/password_reset_done.html'),name = 'password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='students/password_reset.html'),name = 'password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='students/password_reset_complete.html'),name = 'password_reset_complete'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    ]
