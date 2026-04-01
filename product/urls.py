from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    # 1. RUTAS FIJAS (Prioridad máxima)
    path('', views.product_list, name='product_list'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'), 
    path('ofertas/', views.ofertas, name='ofertas'),
    path('servicio-cliente/', views.servicio_cliente, name='servicio_cliente'),

    # 2. RUTAS DE LA API
     path('ofertas/', views.ofertas, name='ofertas'), 
    path('api/latest-products/', views.LatestProductsList.as_view()),
    path('api/search/', views.search),
    path('api/products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    path('api/category/<slug:category_slug>/', views.CategoryDetail.as_view()),

    # 3. RUTAS DINÁMICAS (Al final para que no "roben" tráfico)
    path('item/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('<slug:category_slug>/', views.category_detail, name='category_detail'),
]


