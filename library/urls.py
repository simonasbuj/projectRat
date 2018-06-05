from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('knygos/', views.index, name='index'),
    path('knyga/<slug:slug>/', views.book_details, name='book_details'),
    path('test/', views.test, name='test'),
]