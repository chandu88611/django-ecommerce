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
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def create_product(request):
    try:
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product=Product.objects.create(**request.data,user=request.user)
            res=ProductSerializer(product,many=False)
            response_data = {
                "message": "Product created successfully",
                "status": True,
                "data":res.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                "message": "Product creation failed",
                "errors": serializer.errors,
                "status": False
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        response_data = {
            "message": f"Product creation failed: {str(e)}",
            "status": False
        }
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_products(request):
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