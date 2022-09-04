from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategorySerializer, GetCategorySerializer, AddProductSerializer, ProductSerializer, \
    AddOrderSerializer, OrderGnerateSerializer, UpdateOrderSerializer, UpdateProductSerializer
from .services import CategoryService, UpdateCategoryService, AddProductService, UpdateProductService, AddOrderService, \
    UpdateOrderService
from .models import Category, Product, Order
from base_model.constants import (
    PUBLIC_ID,
    RESULT,
    ERROR,
    SUCCESS,
    CATEGORY_DOEST_NOT_CREATE,
    CATEGORY_IS_UPDATED,
    CATEGORY_IS_DELETED,
    CATEGORY_DOES_NOT_EXIST,
    PRODUCT_NOT_CREATED,
    PRODUCT_DOES_NOT_EXIST,
    PRODUCT_IS_DELETED,
    ORDER_DOES_NOT_EXIST,
    ORDER_IS_DELETED,
)


class AddCategoryView(APIView):
    def post(self, request):
        serialized_data = CategorySerializer(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            parsed_data = serialized_data.validated_data
            category_id = CategoryService.execute({
                "name": parsed_data["name"],
                "status": parsed_data["status"]
            })
            return Response({PUBLIC_ID: category_id}, status=status.HTTP_200_OK)
        return Response({ERROR: CATEGORY_DOEST_NOT_CREATE}, status=status.HTTP_400_BAD_REQUEST)


class GetCategory(APIView):
    def get(self, request):
        try:
            category = Category.objects.all()
            serial_data = GetCategorySerializer(category, many=True)
            return Response({RESULT: serial_data.data}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({ERROR: CATEGORY_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)


class DetailCateory(APIView):
    def get(self, request, public_id):
        try:
            category = Category.objects.get(public_id=public_id)
            serial_data = GetCategorySerializer(category)
            return Response({RESULT: serial_data.data}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({ERROR: CATEGORY_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)


class DeleteCategory(APIView):
    def delete(self, request, public_id):
        try:
            category = Category.objects.get(public_id=public_id)
            category.delete()
            return Response({RESULT: CATEGORY_IS_DELETED}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({ERROR: CATEGORY_DOES_NOT_EXIST}, status=status.HTTP_400_BAD_REQUEST)


class UpdateCategory(APIView):
    def patch(self, request, public_id):
        try:
            # breakpoint()
            category = Category.objects.get(public_id=public_id)
            serial_data = CategorySerializer(data=request.data)
            if serial_data.is_valid(raise_exception=True):
                serialized_data=serial_data.validated_data
                name = serialized_data.get("name")
                status = serialized_data.get("status")
                UpdateCategoryService.execute({
                    "name": name,
                    "status": status,
                    "category": category,
                })
            return Response({RESULT: CATEGORY_IS_UPDATED}, HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({ERROR: CATEGORY_DOES_NOT_EXIST},HTTP_400_BAD_REQUEST)


class AddProducts(APIView):
    def post(self, request, public_id):
        try:
            category = Category.objects.get(public_id=public_id)
            serializer = AddProductSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serialized_data = serializer.validated_data
                name = serialized_data["name"]
                price = serialized_data["price"]
                category = category
                status = serialized_data["status"]
                public_id = AddProductService.execute({
                    "name": name,
                    "price": price,
                    "category": category,
                    "status": status,
                })
                return Response({PUBLIC_ID: public_id}, HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({ERROR: CATEGORY_DOES_NOT_EXIST}, HTTP_400_BAD_REQUEST)


class GetProducts(APIView):
    def get(self, request):
        try:
            product = Product.objects.all()
            serial_data = AddProductSerializer(product, many=True)
            return Response({RESULT: serial_data.data}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({ERROR: PRODUCT_DOES_NOT_EXIST}, status=status.HTTP_200_OK)


class DetailProduct(APIView):
    def get(self, request, public_id):
        try:
            product = Product.objects.get(public_id=public_id)
            serial_data = ProductSerializer(product)
            return Response({RESULT: serial_data.data}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({ERROR: PRODUCT_DOES_NOT_EXIST}, status=status.HTTP_200_OK)


class UpdateProduct(APIView):
    def patch(self, request, public_id):
        # breakpoint()
        serial_data = UpdateProductSerializer(data=request.data)
        if serial_data.is_valid(raise_exception=True):
            serialized_data = serial_data.validated_data
            product_public_id = UpdateProductService.execute({
            "name": serialized_data.get("name"),
            "price": serialized_data.get("price"),
            "status": serialized_data.get("status"),
            "product": public_id,
        })
            return Response({PUBLIC_ID: product_public_id}, status=status.HTTP_201_CREATED)


class DeleteProduct(APIView):
    def delete(self, request, public_id):
        try:
            product = Product.objects.get(public_id=public_id)
            product.delete()
            return Response({RESULT: PRODUCT_IS_DELETED}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({ERROR: PRODUCT_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)


class AddOrder(APIView):
    def post(self, request, product_public_id):
        try:
            product = Product.objects.get(public_id=product_public_id)
            serialize_data = AddOrderSerializer(data=request.data)
            if serialize_data.is_valid(raise_exception=True):
                serialized_data = serialize_data.validated_data
                order_public_id = AddOrderService.execute({
                    "quantity": serialized_data["quantity"],
                    "status": serialized_data["status"],
                    "product": product,
                })
            order = Order.objects.get(public_id=order_public_id)
            products = OrderGnerateSerializer(product, context={"order": order})
            return Response({
                            "order_id": order.public_id,
                            "name": products.data["name"],
                            "status": order.status,
                            "price": products.data["price"],
                            "quantity": order.quantity,
                            "total_price": products.data["total_price"],
                             }
                            , status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response({ERROR: PRODUCT_DOES_NOT_EXIST}, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({ERROR: ORDER_DOES_NOT_EXIST}, status=status.HTTP_400_BAD_REQUEST)



# class UpdateOrder(APIView):
#     def patch(self,request,public_id,product_public_id):
#         # breakpoint()
#         serial_data = UpdateOrderSerializer(data=request.data)
#         if serial_data.is_valid(raise_exception=True):
#             order = Order.objects.get(public_id=public_id)
#             product = Product.objects.get(public_id=product_public_id)
#             serialized_data = serial_data.validated_data
#             order_update = UpdateOrderService.execute({
#                 "product": product,
#                 "quantity":serialized_data.data["quantity"] if serialized_data.data["quantity"] else "",
#                 "order": order,
#                 "status": serialized_data.data["status"] if serialized_data.data["status"] else "",
#                 "is_status": serialized_data.data["is_status"] if serialized_data.data["is_status"] else "",
#                 "cancel_order": serialized_data.data["cancel_order"] if serialized_data.data["cancel_order"] else "",
#             })
#             return Response({"id":order_update})



class DeleteOrder(APIView):
    def delete(self, request, public_id):
        try:
            order = Order.objects.get(public_id=public_id)
            order.delete()
            return Response({RESULT: ORDER_IS_DELETED}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({ERROR: ORDER_DOES_NOT_EXIST}, status=status.HTTP_404_NOT_FOUND)
