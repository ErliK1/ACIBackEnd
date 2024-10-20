from rest_framework.response import Response
from rest_framework import status

from django.http import Http404
from django.db.models import Sum, F

from shared.views import ACICreateAPIView, ACIListAPIView, ACIListCreateAPIView
from product.models import Order, Product, OrderProduct
from shared.constants import *

from datetime import datetime


class OrderCreateListFromManagerAPIView(ACIListCreateAPIView):
    queryset = Order.objects.all()
    write_serializer_class = None
    read_serializer_class = None
    filter_map = {}
    filter_serializer_class = None


    def get_queryset(self):
        query_params = self.request.query_params
        order_queryset = Order.objects.all()
        if query_params.get('product_name'):
            order_queryset = order_queryset.filter(order_products__product__name__icontains=query_params.get('product_name'))
        if query_params.get('sku_code'):
            order_queryset = order_queryset.filter(order_products__product__sku_code=query_params.get('sku_code'))
        if query_params.get('transaction_time'):
            transaction_datetime = datetime.strptime(query_params.get('transaction_time'), DATETIME_FORMAT)
        if query_params.get('max_price'):
            pass
        return query_params

