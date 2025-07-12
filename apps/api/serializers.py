from .models import Interpretation
from rest_framework import serializers

class InterpretationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interpretation
        fields = '__all__'
        read_only_fields = ('interpretation', 'created_at')