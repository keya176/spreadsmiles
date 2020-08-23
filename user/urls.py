from django.urls import path
from . import views

urlpatterns = [
    
    path('register/', views.register),
    path('login/', views.loginuser),
    path('logout/', views.logoutpage),

    path('', views.home, name="home"),
    path('about/', views.about),
    path('gallary/', views.gallary),
    path('allevents/', views.allevents),
    path('donatemoney/<str:pk>/', views.donatemoney),
    path('payment/<str:pk>/', views.payment, name="pay"),
    path('status/', views.complete, name="status"),
    path('donatebelongings/', views.donatebelongings),
    path('orghome/<str:pk>/', views.orghome, name="back"),
    path('adminhome/<str:pk>/', views.adminhome, name="admin"),
    path('event/<str:pk>/', views.singleevent, name="event"),
    path('create_event/', views.create_event),
    path('update_event/<str:pk>/', views.update_event),
    path('delete_event/<str:pk>/', views.delete_event),

]
