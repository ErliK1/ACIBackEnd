from rest_framework import serializers

from product.models import Product, Brand, Category, ProductCategory
from shared.utils import check_ids_part_of_db
from shared.exception import ACIValidationError


class BrandSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Brand
        fields = ('id', 'name', 'country', 'description')
        extra_kwargs = {
                    'id': {'read_only': True},
                }

class ProductCreateSerializer(serializers.ModelSerializer):
    category = serializers.ListField(child=serializers.IntegerField())
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'sku_code', 'buy_price', 'sell_price',
                  'description', 'brand', 'stock', 'discount', 'main_image')
        extra_kwargs = {
                    'id': {'read_only': True}
                }

    def validate(self, data):
        list_of_category_ids = data.get('category')
        if not check_ids_part_of_db(list_of_category_ids, Category):
            raise ACIValidationError("Kategorite e dhena nuk gjenden!")

    def create(self, validated_data):
        category_ids = validated_data.pop('category')
        product = Product.objects.create(**validated_data)
        map(lambda x: ProductCategory.objects.create(product=product, category_id=x), category_ids)
        return product



        
