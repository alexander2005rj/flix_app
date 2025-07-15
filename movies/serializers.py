from django.db.models import Avg
from rest_framework import serializers
from movies.models import Movie
    

class MovieSerializer(serializers.ModelSerializer):
    """
    Criando um campo calculado somente leitura (SerializerMethodField) de média de estrelas
    """
    rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
       model = Movie
       fields = '__all__'

    """
    Criando um método para retornar a média de estrelas
    Método sempre começa com get_<nome_campo>
    """
    def get_rate(self, obj):
        rate = obj.reviews.aggregate(Avg('stars'))['stars__avg']
        
        if rate:
            return round(rate, 1)

        return None

    """
    Criando uma função de validação de Release Date
    Método sempre começa com validate_<nome_campo>
    """
    def validate_release_date(self, value):
       if value.year < 1900:
           raise serializers.ValidationError('A data de lançamento não pode ser anterior a 1900.')
       return value
    
    """
    Criando uma função para validar o tamanho do campo Resume
    """
    def validate_resume(self, value):
        if len(value) > 500:
            raise serializers.ValidationError('Resumo não deve passar de 500 caracteres.')