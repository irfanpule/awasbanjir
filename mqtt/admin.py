from django.contrib import admin
from mqtt.models import MQTTBroker


class AdminMQTTBroker(admin.ModelAdmin):
    list_display = ('broker', 'port', 'username')
    search_fields = ('broker', 'username')


admin.site.register(MQTTBroker, AdminMQTTBroker)
