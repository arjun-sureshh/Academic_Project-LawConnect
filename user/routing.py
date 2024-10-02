from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('contact_lawyer/<int:id>/', consumers.ChatConsumer.as_asgi()),
    path('lawyer/contact_clients/', consumers.ChatConsumer.as_asgi()),
]