from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.decorators import login_required

@login_required
class UrlExempleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return  Response({"Situacao": "Logado"})  # Para usuários autenticados


# from .auth import CustomTokenAuthentication  # Mantenha se necessário

# class CustomLoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)
        
#         if user:
#             token, _ = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key}, status=status.HTTP_200_OK)  # ⬅️ Token no JSON
            
#         return Response(
#             {'error': 'Credenciais inválidas'},
#             status=status.HTTP_400_BAD_REQUEST
#         )
        
        
# class UrlExempleView(APIView):
#     authentication_classes = [CustomTokenAuthentication]  
#     permission_classes = [IsAuthenticated]  

#     def get(self, request):
#         return Response({
#             'message': 'Autenticação confirmada!',
#             'user': request.user.username
#         })

# class HomeExempleView(APIView):
#     authentication_classes = [CustomTokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         return Response({'message': f'Bem-vindo, {request.user.username}!'})