from django.urls import path
from . import views

app_name = 'entertainment'
urlpatterns = [
    path('knygnesys/', views.fundbook, name='fundbook'),
    #path('knyga/<slug:slug>/', views.book_details, name='book_details'),
    path('knygnesys/addwish/', views.addwish, name='addwish'),
    path('knygnesys/payment', views.payment, name='payment'),

    path('tinder/', views.tinder, name='tinder'),
    path('tinder/like', views.like_book, name='like_book'),
    path('tinder/dislike', views.dislike_book, name='dislike_book'),

]
