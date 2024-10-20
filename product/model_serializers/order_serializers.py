from rest_framework import serializers

from product.models import Product, OrderProduct, Order


class OrderSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = Order
        fields = ('id', 'client_secret', 'printed_receipt',
                  'name', 'email', 'address', 'is_admin', 'is_paid_online')
        extra_kwargs = {
                    'id': {'read_only': True},
                    'is_paid_online': {'read_only': True}
                }


