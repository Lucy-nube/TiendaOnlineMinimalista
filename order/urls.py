from django.urls import path
from order import views

app_name = 'order'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('order/', views.OrderList.as_view(), name='order-list'),
]
