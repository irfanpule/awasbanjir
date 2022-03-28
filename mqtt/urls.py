from django.urls import path
from mqtt import views

app_name = 'mqtt'
urlpatterns = [
    path('server-config/', views.MQTTServerUpdateView.as_view(), name='mqtt_server_config'),
]
