from django.urls import path
from .views import *

urlpatterns = [
    path('', admin_login, name='admin_login'),
    path('admin-home', admin_home, name='admin_home'),
    path('add-court/', addcourt, name='addcourt'),
    path('view_all_court/', view_all_court, name='view_all_court'),
    path('view_all_lawyers/', view_all_lawyers, name='view_all_lawyers'),
    path('edit_court/',edit_court,name='edit_court'),
    path('delete_court/',delete_court,name='delete_court'),
    path('add-law/', addlaw, name='addlaw'),
    path('view_all_law/', view_all_law, name='view_all_law'),
    path('delete_law/',delete_law,name='delete_law'),
    path('edit_law/', edit_law, name='edit_law'),
    path('approve_lawyer/', approve_lawyer, name='approve'),
    path('reject_lawyer/', reject_lawyer, name='reject'),
    path('admin_logout/', admin_logout, name='admin_logout'),
]
