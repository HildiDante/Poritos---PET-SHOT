from rest_framework import serializers
from loja.models import Compra

class CompraSerializer(serializers.ModelSerializer):
    data_formatada = serializers.SerializerMethodField()

    class Meta:
        model = Compra
        fields = ['id', 'produto', 'quantidade', 'valor', 'data_formatada']

    def get_data_formatada(self, obj):
        return obj.data.strftime("%d/%m/%Y %H:%M:%S")