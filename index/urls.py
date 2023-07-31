from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_home, name='home'),
    path('login/', views.display_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup', views.display_signup, name='sign_up'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]
