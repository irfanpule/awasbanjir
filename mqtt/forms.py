from django import forms
from mqtt.models import MQTTBroker


class MQTTServerForm(forms.ModelForm):
    class Meta:
        model = MQTTBroker
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput()
        }
