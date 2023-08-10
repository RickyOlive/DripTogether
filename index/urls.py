from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.display_home, name='home'),
    path('login/', views.display_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.display_signup, name='sign_up'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'), name='password_reset_complete'),

]
