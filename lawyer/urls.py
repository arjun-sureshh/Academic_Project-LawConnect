from django.urls import path
from .views import *

urlpatterns = [
    path('', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('home/', home, name='home'),
    path('profile/', lawyerprofile, name='lawyer_profile'),
    path('view_clients/', view_clients, name='view_clients'),
    path('lawyer_view_laws/', lawyer_view_laws, name='lawyer_view_laws'),
    path('lawyer_view_court/', lawyer_view_court, name='lawyer_view_court'),
    path('contact_clients/', contact_clients, name='contact_clients'),
    path('view_lawyer_profile/', view_lawyer_profile, name='view_lawyer_profile'),
    path('edit_lawyer_profile/', edit_lawyer_profile, name='edit_lawyer_profile'),
    path('user_requests/',user_requests, name='user_requests'),
    path('resetp/', resetp, name='resetp'),
    path('forgotp/', forgotp, name='forgotp'),
]
