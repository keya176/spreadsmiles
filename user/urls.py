from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage),
    path('login/', views.loginPage),
    path('logout/', views.logoutUser),

    path('', views.home, name="home"),
    path('about/', views.about),
    path('gallary/', views.gallary),
    path('upgallary/', views.upgallary),
    path('allevents/', views.allevents, name='events'),
    path('moneyevents/', views.moneyevents, name='events'),
    path('bevents/', views.bevents, name='events'),
    path('bothevents/', views.bothevents, name='events'),
    path('donatemoney/<str:pk>/', views.donatemoney),
    path('payment/<str:pk>/', views.payment, name="pay"),
    path('status/', views.complete, name="status"),
    path('donatebelongings/<str:pk>/', views.donatebelongings),
    path('orghome/<str:pk>/', views.orghome, name="back"),
    path('adminpickup/<str:pk>/', views.adminpickup),
    path('event/<str:pk>/', views.singleevent, name="event"),
    path('create_event/', views.create_event),
    path('update_event/<str:pk>/', views.update_event, name='update'),
    path('delete_event/<str:pk>/', views.delete_event),

    path('adminhome/<str:pk>/', views.adminhome, name="admin"),
    path('approve/<str:pk>/', views.apporg),
    path('deapprove/<str:pk>/', views.deapporg),

]
