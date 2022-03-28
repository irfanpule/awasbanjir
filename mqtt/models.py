from django.db import models


class MQTTBroker(models.Model):
    broker = models.CharField(max_length=200)
    port = models.IntegerField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.broker

    @classmethod
    def get_config(cls):
        obj = cls.objects.last()
        if not obj:
            obj = cls.objects.create(broker='', port=1883, username='', password='')
        return obj
