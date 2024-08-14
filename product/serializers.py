from rest_framework import serializers

from product.models import Product, Brand, Category, ProductCategory

class ProductListFilterSerializer(serializers.Serializer):
    category = serializers.ListField(child=serializers.IntegerField,
                                     allow_null=True, allow_blank=True)
    brand = serializers.CharField(allow_null=True, allow_blank=True)
    name = serializers.CharField(allow_null=True, allow_blank=True)
    discount = serializers.BooleanField(allow_null=True, allow_blank=True)

class BrandProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name')

class CategoryProductListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='category.id')
    name = serializers.CharField(source='category.name')

    class Meta:
        model = ProductCategory
        fields = ('id', 'name')


class ProductListSerializer(serializers.ModelSerializer):
    brand = BrandProductListSerializer()
    category = CategoryProductListSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'brand', 'category', 'sell_price') 

