from django.shortcuts import render
from django.shortcuts import render
from rest_framework import generics, status
import rest_framework
from .serializers import  BookSerializer, ProducSerializer, CreateSkartUserSerializer, UpdateSkartUserSerializer
from .models import  Book, Product, SkartUser
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable, ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django.contrib.auth.hashers import make_password


# Create your views here.


class ListBook(generics.ListAPIView):
    queryset =Book.objects.all()
    serializer_class = BookSerializer

class DetailBook(generics.RetrieveAPIView):
    queryset =Book.objects.all()
    serializer_class = BookSerializer

class ListProduct(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProducSerializer

class DetailProduct(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProducSerializer

class CreateSkartUser(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        if request.data is None:
            return NotAcceptable(detail="No data Provided")
        password1 = request.data['user']['password1']
        password2 = request.data['user']['password2']
        if password1 != password2:
            raise NotAcceptable(detail="Passwords did not mat['user']['password']ch.")
        if len(str(password1)) < 8:
            raise NotAcceptable(detail= "Password must contain at least 8 characters")
        if password1.isdigit():
            raise NotAcceptable(detail="password must contain alphabets.")
        else:
            request.data['user']['password'] = password1
            del password1
            del password2
        return super().create(request, *args, **kwargs)
    queryset = SkartUser.objects.all()
    serializer_class = CreateSkartUserSerializer

class UpdateSkartUser(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return SkartUser.objects.filter(user_id= int(self.request.user.id)).select_related('user')
    serializer_class = UpdateSkartUserSerializer
    permission_classes = [IsAuthenticated]


