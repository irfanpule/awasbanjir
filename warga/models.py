from django.db import models
from django.contrib.auth import get_user_model
from awasbanjir.models import BaseModel


class Warga(BaseModel):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    nama_desa = models.CharField(max_length=220)
    no_hp = models.CharField('No. Hp', max_length=20, help_text='No. Hp aktif yang terdaftar ke WA/Telegram')

    def __str__(self):
        return self.nama_desa
