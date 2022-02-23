from rest_framework import serializers
from perangkat.models import DataSeries


class DataSeriesSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    perangkat = serializers.SerializerMethodField()

    class Meta:
        model = DataSeries
        fields = '__all__'

    def get_perangkat(self, obj):
        return str(obj.perangkat.device_id)

    def get_status(self, obj):
        return obj.get_status_display()
