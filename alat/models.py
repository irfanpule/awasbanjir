import uuid
from collections import namedtuple
from django.db import models
from django.contrib.auth import get_user_model
from awasbanjir.models import BaseModel


STATUS_BENCANA = namedtuple(
    'STATUS_BENCANA', 'normal waspada siaga awas'
)._make(range(4))


class Alat(BaseModel):
    nama = models.CharField('Nama', max_length=220, help_text='Mis. Pendeteksi Banjir')
    tipe = models.CharField('Tipe', max_length=100, null=True, blank=True, help_text='Mis. Arduino Uno')
    unique_id = models.UUIDField(default=uuid.uuid4(), editable=False)
    lokasi = models.TextField('Lokasi', help_text='Isi dengan alamat dimana alat tsb dipasang.')
    pemilik = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    batas_normal = models.FloatField(default=0)
    batas_waspada = models.FloatField(default=0)
    batas_siaga = models.FloatField(default=0)
    batas_awas = models.FloatField(default=0)

    def __str__(self):
        return self.nama


class DataSeries(BaseModel):
    STATUS = [
        (STATUS_BENCANA.normal, 'normal'),
        (STATUS_BENCANA.waspada, 'waspada'),
        (STATUS_BENCANA.siaga, 'siaga'),
        (STATUS_BENCANA.awas, 'awas')
    ]
    alat = models.ForeignKey(Alat, on_delete=models.CASCADE)
    jarak = models.FloatField(help_text='Jarak alat ke air (centimeter)')
    status = models.PositiveSmallIntegerField(choices=STATUS, default=STATUS_BENCANA.normal)

    def __str__(self):
        return f'{self.alat} - {self.jarak}'
