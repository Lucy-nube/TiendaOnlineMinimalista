from django.shortcuts import redirect
from rest_framework.views import APIView  
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Order, OrderItem
from .serializers import MyOrderSerializer
from product.models import Product 

# 1. MANAGEMENT PANEL (For the teacher)
class OrderList(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        orders = Order.objects.all()
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)


# 2. REAL CHECKOUT
def checkout(request):
    if request.method == 'POST':
        # Grab cart from session
        cart = request.session.get('cart', {})
        
        if not cart:
            return redirect('product:cart')

        # Create the base order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            first_name=request.POST.get('first_name', 'Client'),
            stripe_token='offline'
        )

        total_amount = 0
        # Loop through cart session items
        for item_id, item_data in cart.items():
            product = Product.objects.get(id=item_id)
            price = float(item_data['price'])
            quantity = int(item_data['quantity'])
            
            OrderItem.objects.create(
                order=order,
                product=product,
                price=price,
                quantity=quantity
            )
            total_amount += price * quantity

        # Save total calculated price
        order.paid_amount = total_amount
        order.save()

        # 🔥 CLEAR THE CART (The requested fix)
        request.session['cart'] = {}
        request.session.modified = True

        return redirect('product:success')

    return redirect('product:cart')
