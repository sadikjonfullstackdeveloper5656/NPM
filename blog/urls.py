from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('add/product/', ProductCreateView.as_view(), name='add_product'),
    path('product/<int:pk>/', DetailProduct.as_view(), name="product_detail"),
    path('add/category/', CategoryView.as_view(), name='category'),
    path('add/order/', OrderCreateView.as_view(), name='order'),
    path('add/customer/', CustomerView.as_view(), name='customer'),
]
