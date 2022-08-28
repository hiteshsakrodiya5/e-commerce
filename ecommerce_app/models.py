from django.db import models
import uuid


class CreateUpdateDate(models.Model):
    class Meta:
        abstract = True

    # Save date and time of add and update.
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class UniqueIds(models.Model):
    class Meta:
        abstract = True

    id = models.BigAutoField(primary_key=True, unique=True)
    #  public id to share with the in url,
    #  Used for REST routes and public displays
    public_id = models.BigIntegerField(null=True, editable=False, unique=True)


class PublicId:
    # method for generating public id
    @staticmethod
    def create_public_id():
        public_id = uuid.uuid4().int >> 75
        return public_id


class Base(CreateUpdateDate,UniqueIds):
    class Meta:
        abstract = True
    
    pass


class Category(Base):
    class Meta:
        db_table = "category"
    name = models.CharField(max_length=150, null=False)
    status = models.CharField(null=True, max_length=150,choices=(("active","active"),("inactive","inactive")))


class Product(Base):
    class Meta:
        db_table = "product"
    name = models.CharField(max_length=150, null=False)
    price = models.IntegerField(null=False)
    category = models.ForeignKey(Category(), on_delete=models.CASCADE)
    status = models.CharField(null=True, max_length=150, choices=(("active", "active"), ("inactive", "inactive")))


class Order(Base):
    class Meta:
        db_table = "order"
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    status = models.CharField(max_length=150, null=False, choices=(
        ("ok", "ok"),
        ("pending", "pending"),
        ("failed", "failed"),
    ))
    is_status = models.CharField(null=True, max_length=150, choices=(("active", "active"), ("inactive", "inactive")))
    cancel_order = models.DateTimeField(default=None)
