from rest_framework.response import Response
from rest_framework import status

from django.db import transaction

from shared.constants import *
from shared.views import ACICreateAPIView, ACIListAPIView, ACIListCreateAPIView, ACIRetrieveAPIView
from product.models import Product, Category, Brand
from product.model_serializers.product_serializers import ProductCreateSerializer, CategorySerializer, BrandSerializer


class ProductCreateAPIView(ACICreateAPIView):
    query_set = Product.objects.all()
    serializer_class = ProductCreateSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({DETAIL: 'Produkti u krijua me suksses'}, status=status.HTTP_201_CREATED)



class CategoryCreateListAPIView(ACIListCreateAPIView):
    queryset = Category.objects.all()
    write_serializer_class = CategorySerializer
    read_serializer_class = CategorySerializer



class BrandCreateListAPIView(ACIListCreateAPIView):
    queryset = Brand
    read_serializer_class = BrandSerializer
    write_serializer_class = BrandSerializer

