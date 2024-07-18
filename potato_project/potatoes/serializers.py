from rest_framework.serializers import ModelSerializer
from .models import Potato


class PotatoSerializer(ModelSerializer) :
    class Meta :
        model = Potato
        fields = '__all__'
         