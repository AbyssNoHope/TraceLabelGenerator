from rest_framework import serializers

from .models import SpanInformation, TraceInformation


class SpanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpanInformation
        fields = '__all__'


class TraceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TraceInformation
        fields = '__all__'
