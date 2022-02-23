from rest_framework import serializers
from alat.models import DataSeries


class DataSeriesSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    alat = serializers.SerializerMethodField()

    class Meta:
        model = DataSeries
        fields = '__all__'

    def get_alat(self, obj):
        return str(obj.alat.unique_id)

    def get_status(self, obj):
        return obj.get_status_display()
