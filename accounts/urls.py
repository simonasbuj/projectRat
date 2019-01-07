from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('logout/', views.logout, name='logout'),
    path('login/', views.login_view, name='login'),
     path('login_old/', views.login_old_view, name='login_old'),


    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/nustatymai/', views.settings, name='settings'),




]
