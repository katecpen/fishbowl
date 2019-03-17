from rest_framework import serializers
from condition.models import condition

class conditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = condition
        fields = ('temperature', 'ph')