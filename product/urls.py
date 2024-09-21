from django.urls import path
from django.urls import include

from product.model_views.product_views import ProductCreateAPIView
from product.url_constans import *

urlpatterns = [
    path('create/', ProductCreateAPIView.as_view(), name=PRODUCT_CREATE),
] 
