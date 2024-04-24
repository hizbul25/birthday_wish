from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Customer
from .serializers import CustomerSerializer

# Create your views here.


class CustomerCreateViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
