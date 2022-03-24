import uuid
import json
from collections import namedtuple

from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

from awasbanjir.models import BaseModel
from mqtt.publisher import publish
from mapbox_location_field.models import LocationField


STATUS_BENCANA = namedtuple(
    'STATUS_BENCANA', 'normal waspada siaga awas'
)._make(range(4))


class Perangkat(BaseModel):
    nama = models.CharField('Nama', max_length=220, help_text='Mis. Pendeteksi Banjir')
    tipe = models.CharField('Tipe', max_length=100, null=True, blank=True, help_text='Mis. Arduino Uno')
    device_id = models.UUIDField(default=uuid.uuid4(), editable=False)
    lokasi = LocationField(map_attrs={"center": [115.64105190308777, -0.5163104314298437], "marker_color": "blue", "zoom": 2})
    pemilik = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    batas_normal = models.FloatField(default=250, help_text='Diisi dalam satuan centimeter (cm)')
    batas_waspada = models.FloatField(default=0, help_text='Diisi dalam satuan centimeter (cm)')
    batas_siaga = models.FloatField(default=0, help_text='Diisi dalam satuan centimeter (cm)')
    batas_awas = models.FloatField(default=0, help_text='Diisi dalam satuan centimeter (cm)')
    beep_alert = models.BooleanField(default=True, help_text='Bunyikan alert pada perangkat')

    def __str__(self):
        return self.nama

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        msg = json.dumps({
            "beep_alert": int(self.beep_alert),
            "waspada": self.batas_waspada,
            "device_id": str(self.device_id)
        })

        publish(
            topic=settings.TOPICS["send_config"],
            msg=msg
        )


class DataSeries(BaseModel):
    STATUS = [
        (STATUS_BENCANA.normal, 'normal'),
        (STATUS_BENCANA.waspada, 'waspada'),
        (STATUS_BENCANA.siaga, 'siaga'),
        (STATUS_BENCANA.awas, 'awas')
    ]
    perangkat = models.ForeignKey(Perangkat, on_delete=models.CASCADE)
    jarak = models.FloatField(help_text='Jarak perangkat ke air (centimeter)')
    status = models.PositiveSmallIntegerField(choices=STATUS, default=STATUS_BENCANA.normal)

    def __str__(self):
        return f'{self.perangkat} - {self.jarak}'

    def set_status(self):
        if self.perangkat.batas_waspada >= self.jarak > self.perangkat.batas_siaga:
            self.status = STATUS_BENCANA.waspada
        elif self.perangkat.batas_siaga >= self.jarak > self.perangkat.batas_awas:
            self.status = STATUS_BENCANA.siaga
        elif self.jarak <= self.perangkat.batas_awas:
            self.status = STATUS_BENCANA.awas
        else:
            self.status = STATUS_BENCANA.normal
        self.save()
