from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

app_name = 'TSMain'
urlpatterns = [
    path('', views.Index, name='Index'),
    path('SignIn/', views.SignIn, name='SignIn'),
    path('SignUp/', views.SignUp, name='SignUp'),
    path('SignOut/', views.SignOut, name='SignOut'),
    path('CreateTask/', views.CreateTask, name='CreateTask'),
    path('ModifyTask/<str:TaskName>/', views.ModifyTask, name='ModifyTask'),
    path('UpdateTask/<str:TaskName>/', views.UpdateTask, name='UpdateTask'),
    path('RemoveAccount/', views.RemoveAccount, name='RemoveAccount'),
    path('SignIn/ResetPassword/', views.ResetPassword, name='ResetPassword')
]

urlpatterns += staticfiles_urlpatterns()