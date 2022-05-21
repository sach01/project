from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('duplicate', views.duplicate, name='duplicate'),
    path('duplicate1', views.duplicate1, name='duplicate1'),
    path('duplicate2', views.duplicate2, name='duplicate2'),
    path('final', views.final, name='final'),
    path('final1', views.final1, name='final1'),
    path('final2', views.final2, name='final2'),
    path('vacant', views.vacant, name='vacant'),
    path('vacant1', views.vacant1, name='vacant1'),
    path('vacant2', views.vacant2, name='vacant2'),
    path('gpayment', views.gpayment, name='gpayment'),
   # path('first', views.first, name='first'),
    #path('vacant', views.vacant, name='vacant'),
    #path('second', views.second, name='second'),
    #path('stall', views.stall, name='stall'),
    #path('gfloor', views.gfloor, name='gfloor'),
    path('gpayment', views.gpayment, name='gpayment'),
    #path('<int:pk>/', views.stall, name='stall'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
   # path('<int:question_id>/', views.detail, name='detail'),
]