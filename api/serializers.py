from rest_framework import serializers
from alat.models import DataSeries


class DataSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSeries
        fields = '__all__'
