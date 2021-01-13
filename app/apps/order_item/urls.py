from django.urls import path

from .views import *

urlpatterns = [
    path('', order_item_list, name="list-order-item"),
    path('<int:pk>', order_item_list, name="list-order-item"),
    path('list/', OrderItemListJson.as_view(), name="list-order-item-json"),
    path('list/<int:pk>', OrderItemListJson.as_view(),
         name="list-order-item-json"),
    path('create/', OrderItemCreateView.as_view(), name='create-order-item'),
    path('update/<int:pk>', OrderItemUpdateView.as_view(),
         name='update-order-item'),
    path('delete/<int:pk>', OrderItemDeleteView.as_view(),
         name='delete-order-item'),
]
