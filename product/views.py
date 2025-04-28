

# System imports
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response 
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters

# Local Imports
from .models import *
from .serializers import *
from .pagination import *
from .filter import *


class ProductViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = ProductPagination
    ordering_fields = ['name','price','created_at']
    ordering = ['-created_at']

    def list(self , request):
        products = Product.objects.all()
        paginator = self.pagination_class()
        filtered_products = ProductFilter(request.GET , queryset= products)
        if filtered_products.is_valid():
            products = filtered_products.qs
        
        ordering = request.GET.get('ordering')
        if ordering:
            products = products.order_by(ordering)


        page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(page,many = True)
        return paginator.get_paginated_response(serializer.data)
    
    def create(self , request):
        try:    
            serializer = CreateProductSerializer(data= request.data)
            if serializer.is_valid():
                product = serializer.save()
                return Response(ProductSerializer(product).data , status=status.HTTP_201_CREATED)
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e))
        
    
    def retrieve(self , request , pk=None):
        try:
            product = Product.objects.filter(pk=pk).first()
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"},status= status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def partial_update(self , request , pk=None):
        
        try:
            product = Product.objects.filter(pk=pk).first()
        except Product.DoesNotExist:
            return Response({"detail":"Product not found"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = CreateProductSerializer(product , data = request.data , partial=True)
        if serializer.is_valid():
            updated_product = serializer.save()
            return Response(ProductSerializer(updated_product).data)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self , request , pk=None):

        try:
            product = Product.objects.filter(pk=pk).first()
        except Product.DoesNotExist:
            return Response({"detail":"Product not found"},status=status.HTTP_400_BAD_REQUEST)
        product.delete()
        return Response({"detail":"Product Successfully Deleted"},status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


