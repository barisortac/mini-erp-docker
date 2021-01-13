from django.urls import path

from .views import *

urlpatterns = [
    path('', order_list, name="list-order"),
    path('list/', OrderListJson.as_view(), name="list-order-json"),
    path('create/', OrderCreateView.as_view(), name='create-order'),
    path('update/<int:pk>', OrderUpdateView.as_view(), name='update-order'),
    path('delete/<int:pk>', OrderDeleteView.as_view(), name='delete-order'),
]
