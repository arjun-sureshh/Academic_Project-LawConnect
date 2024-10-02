
from django.urls import path
from .views import *

urlpatterns=[
    path('',guest,name='guest'),
    path('index/',index,name='index'),
    path('signout/',signout,name='signout'),
    path('register/',register,name='register'),
    path('complete_profile/',completeprofile,name='complete_profile'),
    path('login/',usersignin,name='login'),
    path('view_user_profile/',view_user_profile,name='view_user_profile'),
    path('edit_user_profile/',edit_user_profile,name='edit_user_profile'),
    path('Lawyers/',Lawyers,name='Lawyers'),
    path('view_lawyer/',view_lawyer,name='view_lawyer'),
    path('view_court/',view_court,name='view_court'),
    path('view_law/',view_law,name='view_law'),
    path('contact_lawyer/<int:id>/',contact_lawyer,name='contact_lawyer'),
    path('reset/', reset, name='reset'),
    path('forgot/', forgot, name='forgot'),
    path('Directs/',Directs,name='Directs')
]