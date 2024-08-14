from django.shortcuts import render


from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView

from shared.views import ACIListAPIView


from product.models import Product, OrderProduct
from product.serializers import ProductListFilterSerializer
# Create your views here.

from functools import reduce


class ProductListAPIView(ACIListAPIView):
    serializer_class = None
    filter_map = {
            'category': 'product_categories__product__id',
            'brand': 'brand__id',
            'name': 'name',
            'discount': 'has_discount'
        }
    sort_map = {
        'popularity': 'product_popularities__count',

        }
    filter_serializer_class = ProductListFilterSerializer


    def get_queryset(self, ):     
        if self.request.query_params.get('price'):
            price = float(self.request.query_params.get('price'))
            popularity_queryset = Product.aci_objects.filter(sell_price__lte=price)
        else:
            popularity_queryset = Product.aci_objects.all()
        return popularity_queryset


