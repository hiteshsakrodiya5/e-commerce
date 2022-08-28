from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Category, Product, Order


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150, allow_null=True)
    status = serializers.CharField(max_length=150, allow_null=True)


class GetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AddProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150, allow_null=False)
    price = serializers.IntegerField(allow_null=False)
    status = serializers.ChoiceField(allow_null=True,choices=(("active", "active"), ("inactive", "inactive")))


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderGnerateSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_name(self, instance):
        return instance.name

    def get_price(self, instance):
        return instance.price

    def get_total_price(self, instance):
        return self.context["order"].quantity * instance.price

    class Meta:
        model = Product
        fields = ["name", "price", "total_price"]


class AddOrderSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(allow_null=False)
    status = serializers.ChoiceField(allow_blank=False, choices=(
        ("ok", "ok"),
        ("pending", "pending"),
        ("failed", "failed"),
    ))
    class Meta:
        model = Order
        fields = ["quantity","status"]


class UpdateOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'