from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('knygos/', views.index, name='index'),
    path('knyga/<slug:slug>-<int:id>/', views.book_details, name='book_details'),
    path('knyga/<slug:slug>/bookmark', views.bookmark, name='bookmark'),
    path('knyga/<slug:slug>/comment', views.comment, name='comment'),
    path('knyga/<slug:slug>-<int:id>/reservation', views.reservation, name='reservation'),
    path('reservation/<int:id>/answer', views.reservation_answer, name='reservation_answer'),


    path('paieska/', views.search, name='search'),
    path('test/', views.test, name='test'),
    #path('logout/', views.logout_view, name='logout'),
    path('', views.landing, name='landing'),

]
