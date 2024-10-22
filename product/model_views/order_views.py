from rest_framework.response import Response
from rest_framework import status

from django.http import Http404
from django.db.models import Sum, F, Q

from django.db import transaction


from product.model_serializers.order_serializers import OrderCreateForAdminSerializer, OrderCreateForUserSerializer, OrderListSerializer
from shared.views import ACICreateAPIView, ACIListAPIView, ACIListCreateAPIView
from product.models import Order, Product, OrderProduct
from shared.constants import *
from product.utils import check_if_user_is_admin, \
get_the_last_part_of_date_key, parse_string_to_date, get_keys_that_contains_date

from datetime import datetime




class OrderListFromManagerAPIView(ACIListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    filter_map = {
        'name': 'name',
        'email': 'email',
        'address': 'address',
        'phone_number': 'phone_number',
    }
    filter_serializer_class = None

    def get_queryset(self, ):
        list_of_transaction_keys = get_keys_that_contains_date(self.request.query_params.keys())
        query_set = super().get_queryset()
        return self.prepare_queryset_for_date(query_set, list_of_transaction_keys)
    
    def prepare_queryset_for_date(self, query_set, list_of_transaction_keys):
        for element in list_of_transaction_keys:
            last_part = get_the_last_part_of_date_key(element)
            transaction_date = parse_string_to_date(self.request.query_params.get(element))
            data = {
                'transaction_time__' + last_part: transaction_date 
            }
            query_set = query_set.filter(Q(**data))
        return query_set
    
    
    
    
            

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
            

