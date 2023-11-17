from rest_framework import serializers
from .models import Categories, Products, Recommendations


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Categories
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Products
        fields = '__all__'

class RecommendationSerializer(serializers.ModelSerializer):
    #id = serializers.CharField(read_only=True)

    class Meta:
        model = Recommendations
        fields = '__all__'