from django.urls import path

from .views import *

urlpatterns = [
    path('', product_list, name="list-product"),
    path('get/<int:pk>/', get_product, name="get-product"),
    path('list/', ProductListJson.as_view(), name="list-product-json"),
    path('create/', ProductCreateView.as_view(), name='create-product'),
    path('update/<int:pk>', ProductUpdateView.as_view(), name='update-product'),
    path('read/', ProductReadView.as_view(), name='read-product'),
    path('read/<int:pk>', ProductReadView.as_view(), name='read-product'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name='delete-product'),

    path('product_type/', product_type_list, name="list-product-type"),
    path('product_type/list/', ProductTypeListJson.as_view(),
         name="list-product-type-json"),
    path('product_type/create/', ProductTypeCreateView.as_view(),
         name='create-product-type'),
    path('product_type/update/<int:pk>', ProductTypeUpdateView.as_view(),
         name='update-product-type'),
    path('product_type/read/<int:pk>', ProductTypeReadView.as_view(),
         name='read-product-type'),
    path('product_type/delete/<int:pk>', ProductTypeDeleteView.as_view(),
         name='delete-product-type')
]
