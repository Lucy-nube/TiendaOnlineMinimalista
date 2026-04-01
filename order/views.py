from rest_framework.views import APIView  
from rest_framework.response import Response
from .models import Order 
from rest_framework.decorators import api_view
from rest_framework.response import Response

class OrderList(APIView):
    def get(self, request):
        # Aquí puedes devolver la lista de pedidos en el futuro
        return Response({"message": "Lista de pedidos"})



@api_view(['POST'])
def checkout(request):
    # Aquí irá la lógica para procesar el carrito y el pago
    return Response({"message": "Checkout recibido"})
