from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse

from django.contrib import messages

from mqtt.models import MQTTBroker
from mqtt.forms import MQTTServerForm
from awasbanjir.mixin import ContextTitleMixin


@method_decorator(staff_member_required, name='dispatch')
class MQTTServerUpdateView(ContextTitleMixin, UpdateView):
    template_name = 'website/form.html'
    title_page = "MQTT Server"
    form_class = MQTTServerForm

    def get_object(self, queryset=None):
        return MQTTBroker.get_config()

    def post(self, request, *args, **kwargs):
        post = super().post(request, *args, **kwargs)
        messages.success(request, "Berhasil ubah data MQTT Server")
        return post

    def get_success_url(self):
        return reverse("mqtt:mqtt_server_config")
