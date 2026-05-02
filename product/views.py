from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .cart import Cart 

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

class LatestProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})



def product_list(request):
    products = Product.objects.all() 
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('product:product_list')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart_detail.html', {'cart': cart})


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    # Buscamos el producto en la sesión y restamos 1 o lo eliminamos
    p_id = str(product_id)
    if p_id in cart.cart:
        if cart.cart[p_id]['quantity'] > 1:
            cart.cart[p_id]['quantity'] -= 1
        else:
            del cart.cart[p_id]
        cart.save()
    return redirect('product:cart_detail')


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1) # Aquí se ejecuta la magia
    return redirect('product:cart_detail') # Te manda a la bolsa para ver el cambio


def ofertas(request):
    # Aquí podrías filtrar productos con descuento en el futuro
    products = Product.objects.all()[:4] 
    return render(request, 'shop/ofertas.html', {'products': products})

def servicio_cliente(request):
    return render(request, 'shop/servicio_cliente.html')

def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/product_list.html', {
        'category': category,
        'products': products
    })


def success(request):
    return render(request, 'shop/success.html')


def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        # ... lógica de guardar pedido ...
        request.session['cart'] = {} 
        return redirect('product:success') 
    return render(request, 'shop/checkout.html', {'cart': cart})


def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    # Cambiamos el nombre del template aquí:
    return render(request, 'shop/category_detail.html', {
        'category': category,
        'products': products
    })


def ofertas(request):
    # Traemos solo los productos baratos para la sección de ofertas
    products = Product.objects.filter(price__lt=5) 
    return render(request, 'shop/ofertas.html', {'products': products})


from django.db.models import Q # <--- ¡Asegúrate de tener este import arriba!
from django.shortcuts import render
from .models import Product

def product_list(request):
    query = request.GET.get('query', '')
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()
        
    return render(request, 'shop/product_list.html', {
        'products': products,
        'query': query 
    })
