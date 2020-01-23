from .models import *
from rest_framework.serializers import ModelSerializer

class RubricaClientiSerializer(ModelSerializer):
    class Meta:
        model = RubricaClienti
        fields = '__all__'