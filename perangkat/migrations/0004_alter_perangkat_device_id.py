# Generated by Django 4.0.2 on 2022-03-23 15:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('perangkat', '0003_alter_perangkat_batas_awas_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perangkat',
            name='device_id',
            field=models.UUIDField(default=uuid.UUID('91d9a0cf-e2ec-4d64-b3cc-ec30b59c2938'), editable=False),
        ),
    ]