# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user  # Supongamos que el objeto tiene un campo `user`.



class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Hello, authenticated user!'})



class PersonalDataView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request):
        # Lógica para obtener datos personales
        return Response({'message': 'Access granted to personal data!'})