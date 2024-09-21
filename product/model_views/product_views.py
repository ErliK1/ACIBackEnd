from rest_framework.response import Response
from rest_framework import status

from django.db import transaction

from shared.views import ACICreateAPIView, ACIListAPIView, ACIListCreateAPIView, ACIRetrieveAPIView
from product.models import Product
from product.model_serializers.product_serializers import ProductCreateSerializer


class ProductCreateAPIView(ACICreateAPIView):
    query_set = Product.objects.all()
    serializer_class = ProductCreateSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Produkti u krijua me suksses'}, status=status.HTTP_201_CREATED)




