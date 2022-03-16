from django.urls import path

from .views import send_message_to_kafka

app_name = 'core'


urlpatterns = [
    path('send_message_to_kafka/', send_message_to_kafka, name='send-message-to-kafka'),
]
