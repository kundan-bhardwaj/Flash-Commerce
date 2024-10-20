from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer, OrderItemSerializer
from django.shortcuts import render



def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

# Product Views
@api_view(['GET', 'POST'])
def create_product(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def view_update_products(request, pr):
    try:
        product = Product.objects.get(id=pr)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    if request.method == 'PUT':
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Order Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    if request.method == 'GET':
        orders = Order.objects.filter(customer=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=request.user)
            ord = Order.objects.get(id = serializer.data.id)
            for item in ord.orderitem_set.all():
                item.product.stock -= item.quantity
                item.product.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_orders(request, pr):
    try:
        order = Order.objects.get(id=pr)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.user != order.customer and not request.user.is_staff:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    serializer = OrderSerializer(order)
    return Response(serializer.data)

# Order Management Views
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def cancel_order(request, pr):
    if request.method == 'PUT':
        try:
            order = Order.objects.get(id=pr, customer=request.user, status='pending')
        except Order.DoesNotExist:
            return Response({'error': 'Order not found or cannot be canceled'}, status=status.HTTP_404_NOT_FOUND)

        order.status = 'canceled'
        order.save()
        # Restock the products
        for item in order.orderitem_set.all():
            item.product.stock += item.quantity
            item.product.save()

        return Response({'status': 'Order canceled'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def ship_order(request, pr):
    try:
        order = Order.objects.get(id=pr, status='pending')
    except Order.DoesNotExist:
        return Response({'error': 'Order not found or cannot be shipped'}, status=status.HTTP_404_NOT_FOUND)

    order.status = 'shipped'
    order.save()
    return Response({'status': 'Order shipped'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def deliver_order(request, pr):
    try:
        order = Order.objects.get(id=pr, status='shipped')
    except Order.DoesNotExist:
        return Response({'error': 'Order not found or cannot be delivered'}, status=status.HTTP_404_NOT_FOUND)

    order.status = 'delivered'
    order.save()
    return Response({'status': 'Order delivered'}, status=status.HTTP_200_OK)
