from service_objects.services import Service
from .models import Category, PublicId, Product, Order


class CategoryService(Service):
    def process(self):
        name = self.data.get("name")
        status = self.data.get("status")

        catagory = Category.objects.create(
            public_id=PublicId.create_public_id(),
            name=name,
            status=status
        )
        return catagory.public_id


class UpdateCategoryService(Service):
    def process(self):
        # breakpoint()
        name = self.data.get("name")
        status = self.data.get("status")
        category = self.data.get("category")
        if name:
            category.name = name
        if status:
            category.status = status
        category.save()
        return category.public_id


class AddProductService(Service):
    def process(self):
        product = Product.objects.create(
            public_id=PublicId.create_public_id(),
            name=self.data["name"],
            price=self.data["price"],
            status=self.data["status"],
            category=self.data["category"],
        )
        return product.public_id


class UpdateProductService(Service):
    def process(self):
        # breakpoint()
        name = self.data["name"]
        price = self.data["price"]
        status = self.data["status"]
        product = self.data["product"]
        try:
            product = Product.objects.get(public_id=product)
            if name:
                product.name = name
            elif price:
                product.price = price
            elif status:
                product.status = status
            product.save()
            return product.public_id
        except Product.DoesNotExist:
            return "producut does not exist !!"


class AddOrderService(Service):
    def process(self):
        product = self.data["product"]
        quantity = self.data["quantity"]
        status = self.data["status"]
        order = Order.objects.create(
            public_id=PublicId.create_public_id(),
            product=product,
            status=status,
            quantity=quantity,
        )
        return order.public_id


class UpdateOrderService(Service):
    def process(self):
        quantity = self.data["quantity"]
        status = self.data["status"]
        cancel_order = self.data["cancel_order"]
        order = self.data["order"]
        if quantity:
            order.quantity = quantity
        if status:
            order.status = status
        if cancel_order:
            order.cancel_order = cancel_order
        order.save()
        return {}
