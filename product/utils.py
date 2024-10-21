from product.models import Product, Order, OrderProduct

from django.db.models import Sum

from shared.models import ACIAdmin

def find_total_sells_for_product(order_products):
    order_products = order_products.annotate(total_sum=Sum("total_price"))
    return order_products.first().total_price


def check_if_user_is_admin(request):
    return ACIAdmin.objects.filter(user=request.user).exists()
