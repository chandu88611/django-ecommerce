from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import ProductSerializer
from rest_framework import status
from .models import Product
from .filters import ProductFilter
# Create your views here.

@api_view(['GET'])
def get_products(request):
    # products = Product.objects.all()
    # serializer = ProductSerializer(products, many=True)
    filterset=ProductFilter(request.GET,queryset=Product.objects.all().order_by("id"))
    perpage=2
    paginator=PageNumberPagination()
    paginator.page_size=perpage
    queryset=paginator.paginate_queryset(filterset.qs,request)
    serializer = ProductSerializer(queryset, many=True)
    return Response({ "products": serializer.data })

@api_view(['GET'])
def get_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    serializer = ProductSerializer(product)
    return Response({ "product": serializer.data })

@api_view(['DELETE'])
def delete_product(request, pk):
    try:
        product = get_object_or_404(Product, id=pk)
        product.delete()
        response_data = {
            "message": f"Product with ID {pk} was successfully deleted.",
            "status": True
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)
    except:
        response_data = {
            "message": f"Product with ID {pk} does not exist.",
            "status": False
        }
        return Response(response_data, status=status.HTTP_404_NOT_FOUND)