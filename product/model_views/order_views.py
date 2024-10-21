from rest_framework.response import Response
from rest_framework import status

from django.http import Http404
from django.db.models import Sum, F

from django.db import transaction


from product.model_serializers.order_serializers import OrderCreateForAdminSerializer, OrderCreateForUserSerializer
from shared.views import ACICreateAPIView, ACIListAPIView, ACIListCreateAPIView
from product.models import Order, Product, OrderProduct
from shared.constants import *
from product.utils import check_if_user_is_admin

from datetime import datetime




class OrderListFromManagerAPIView(ACIListAPIView):
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
    

class OrderCreateAPIView(ACICreateAPIView):
    queryset = Order.objects.all()
    
    def get_serializer_class(self):
        if check_if_user_is_admin(request=self.request):
            OrderCreateForAdminSerializer
        return OrderCreateForUserSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if (serializer.data.get('printed_receipt')):
            pass
        return Response({MESSAGE: 'Kerkesa U be Me Sukses!'}, status=status.HTTP_201_CREATED)
            

