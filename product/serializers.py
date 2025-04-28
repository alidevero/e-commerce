from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    metadata = serializers.JSONField()
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self,value):
        if value <0:
            raise serializers.ValidationError("Price can not be negative")
        return value
        
    def validate_stock(self , value):
        if value <0:
            raise serializers.ValidationError("Stock can not be negative")
        return value

class CreateProductSerializer(serializers.ModelSerializer):
    metadata = serializers.JSONField()
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['name','description','price','image','category' , 'stock','metadata']


    def validate_name(self,value):
        if not value:
            raise serializers.ValidationError("Name is required")
        return value

    def validate_price(self,value):
        if value <0:
            raise serializers.ValidationError("Price can not be negative")
        return value
        
    def validate_stock(self , value):
        if value <0:
            raise serializers.ValidationError("Stock can not be negative")
        return value

    