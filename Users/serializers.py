from rest_framework import serializers
from .models import Disease

class DiseaseSerializers(serializers.ModelSerializers):
    class Meta:
        model=Disease
        fields='__all__'