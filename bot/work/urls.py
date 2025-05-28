from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

app_name = 'work'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='work/login.html', authentication_form=LoginForm),
         name='login'),
    path('logout/', views.logout_v, name='logout'),
    path('add/', views.add_chats, name='add_group'),
    path('create_session/', views.create_session, name='create_session'),
    path('handle_step2/<int:session_id>/', views.handle_step2, name='handle_step2'),
]
