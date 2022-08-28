from django.urls import path
from . import views
urlpatterns = [
    path("addCategory/", views.AddCategoryView.as_view(), name="add_category"),
    path("getCategory/", views.GetCategory.as_view(), name="get_category"),
    path("detailCategory/<str:public_id>/", views.DetailCateory.as_view(), name="detail_category"),
    path("deleteCategory/<str:public_id>/", views.DeleteCategory.as_view(), name="delete_category"),
    path("updateCategory/<str:public_id>/", views.UpdateCategory.as_view(), name="update_category"),
    path("addProducts/<str:public_id>/", views.AddProducts.as_view(), name="add_product"),
    path("getProduct/", views.GetProducts.as_view(), name="get_product"),
    path("detailProduct/<str:public_id>/", views.DetailProduct.as_view(), name="detail_product"),
    path("updateProduct/<str:public_id>/", views.UpdateProduct.as_view(), name="update_product"),
    path("deleteProduct/<str:public_id>/", views.DeleteProduct.as_view(), name="delete_product"),
    path("addOrder/<str:product_public_id>/", views.AddOrder.as_view(), name="add_order"),
    path("deleteOrder/<str:public_id>/", views.DeleteOrder.as_view(), name="delete_order")
    # path("product/<str:product_public_id>/orderUpddate/<public_id>/", views.UpdateOrder.as_view(), name="update_order"),
]