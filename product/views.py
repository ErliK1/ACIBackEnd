from django.shortcuts import render


from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView

from shared.views import ACIListAPIView


from product.models import Product, OrderProduct
from product.serializers import ProductListFilterSerializer

from product.model_serializers.product_serializers import ProductListSerializer
# Create your views here.

from functools import reduce


class ProductListAPIView(ACIListAPIView):
    serializer_class = ProductListSerializer
    filter_map = {
            'category': 'product_categories__category__id', # list of ids (numbers)
            'brand': 'brand__id', #id (number)
            'name': 'name', # string 
            'discount': 'has_discount', # boolean
        }
    sort_map = {
        'popularity': 'product_popularities__product_count',
        'name': 'name',
        }
    filter_serializer_class = ProductListFilterSerializer


    def get_queryset(self, ):
        popularity_queryset = Product.objects.filter(deleted=False)
        if self.request.query_params.get('lt_price') and self.request.query_params.get('lt_price').isnumeric():
            price = float(self.request.query_params.get('lt_price'))
            popularity_queryset = popularity_queryset.filter(sell_price__lte=price)
        elif self.request.query_params.get('gt_price') and self.request.query_params.get('gt_price').isnumeric():
            price = float(self.request.query_params.get('gt_price'))
            popularity_queryset = popularity_queryset.filter(sell_price__gte=price)
        return popularity_queryset


