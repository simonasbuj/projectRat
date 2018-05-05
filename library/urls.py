from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('knygos/', views.index, name='index'),
]