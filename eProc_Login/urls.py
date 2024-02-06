# URL file for handling '' path (user app)
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'eProc_Login'

# Defining the mapping between URLs and views
urlpatterns = [
    path('', views.login_page, name="login_page"),  # Login page url
    path('login/', views.login_page, name='login_page'),  # Login page url
    path('logout/', views.logout_page, name="logout_page"),  # Logout page url
    path('password/', views.first_time_password_change, name='first_time_password_change'),
    # Change password for first login
    # Forgot password url
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='Forgot_Password/password_reset_form.html',
                                              email_template_name='Forgot_Password/password_reset_email.html',
                                              subject_template_name='Forgot_Password/password_reset_subject.txt'),
         name='password_reset'),

    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='Forgot_Password/password_change_done.html'),
         name='password_change_done'),

    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='Forgot_Password/password_change.html'),
         name='password_change'),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='Forgot_Password/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='Forgot_Password/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='Forgot_Password/password_reset_complete.html'),
         name='password_reset_complete'),

    path('user_locked/', views.user_lock, name='user_locked'),
    path('unlock_user/', views.unlock_user),
    path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('user_details_email/', views.user_details_email, name="user_details_email"),
]
