from decimal import Decimal
from django.conf import settings
from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        # Usamos un nombre fijo para la sesión
        cart = self.session.get('cart')
        if not cart:
            # Si no existe, creamos un diccionario vacío en la sesión
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        # EL ID DEBE SER STRING (Crucial para JSON)
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price) # El precio también como string
            }
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()

    def save(self):
        # ESTA LÍNEA ES LA QUE HACE QUE EL (0) CAMBIE A (1)
        self.session.modified = True

    def __len__(self):
        # Esto es lo que lee {{ cart|length }} en tu HTML
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """
        Recorre los elementos del carrito y recupera los productos de la base de datos.
        """
        product_ids = self.cart.keys()
        # Obtenemos los objetos de los productos y los añadimos al carrito
        products = Product.objects.filter(id__in=product_ids)
        
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
