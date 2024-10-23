from rest_framework import serializers

from product.models import Product, Brand, Category, ProductCategory, ProductImage
from shared.utils import check_ids_part_of_db
from shared.exception import ACIValidationError


class BrandSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Brand
        fields = ('id', 'name', 'country', 'description')
        extra_kwargs = {
                    'id': {'read_only': True},
                }
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'description')
        extra_kwargs = {
                'id': {'read_only': True}
                }

class ProductCreateSerializer(serializers.ModelSerializer):
    category = serializers.ListField(child=serializers.IntegerField())
    images = serializers.ListField(child=serializers.ImageField(), required=False)
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'sku_code', 'buy_price', 'sell_price',
                  'description', 'brand', 'stock', 'discount', 'main_image', 'images')
        extra_kwargs = {
                    'id': {'read_only': True}
                }

    def validate(self, data):
        list_of_category_ids = data.get('category')
        if not check_ids_part_of_db(list_of_category_ids, Category):
            raise ACIValidationError("Kategorite e dhena nuk gjenden!")
        return data

    def create(self, validated_data):
        images = []
        if validated_data.get('images'):
            images = validated_data.pop('images')
        category_ids = validated_data.pop('category')
        product = Product.objects.create(**validated_data)
        for category_id in category_ids:
            ProductCategory.objects.create(product=product, category_id=category_id)
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        return product

class PitagoraListAPIView(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'sku_code', 'buy_price', 'sell_price', '')


        
