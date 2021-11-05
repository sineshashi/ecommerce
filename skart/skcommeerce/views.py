from django.db.models.query import QuerySet
from django.shortcuts import render
from django.shortcuts import render
from rest_framework import generics, status
import rest_framework
from rest_framework.request import Request
from .serializers import  BookSerializer, ProducSerializer, CreateSkartUserSerializer, UpdateSkartUserSerializer, CartSerializer, OrderSerializer
from .models import  Book, Product, SkartUser, Cart, PlaceOrder
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

class SkartUserProfile(generics.RetrieveUpdateDestroyAPIView):
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is None:
            raise NotAcceptable(detail="No data provided.")
        pk_data = SkartUser.objects.get(id = pk)
        user_data = SkartUser.objects.get(user_id = self.request.user.id)
        if pk_data != user_data:
            raise NotAcceptable(detail="You are not authorized for this data")
        return super().retrieve(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is None:
            raise NotAcceptable(detail="No data provided.")
        pk_data = SkartUser.objects.get(id = pk)
        user_data = SkartUser.objects.get(user_id = self.request.user.id)
        if pk_data != user_data:
            raise NotAcceptable(detail="You are not authorized for this data")
        return super().update(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is None:
            raise NotAcceptable(detail="No data provided.")
        pk_data = SkartUser.objects.get(id = pk)
        user_data = SkartUser.objects.get(user_id = self.request.user.id)
        if pk_data != user_data:
            raise NotAcceptable(detail="You are not authorized for this data")
        return super().destroy(request, *args, **kwargs)
    def get_queryset(self):
        return SkartUser.objects.all().select_related('user')
    serializer_class = UpdateSkartUserSerializer
    permission_classes = [IsAuthenticated]


class CartView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        id = self.request.user.id
        user_data = SkartUser.objects.get(user_id = id)
        request.data['user'] = user_data.id
        return super().create(request, *args, **kwargs)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]


class CartUpdateView(generics.RetrieveUpdateAPIView):
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        pk = kwargs.get('pk')
        userid = self.request.user.id
        if pk is None:
            raise NotAcceptable(detail="No data provided.")
        pk_data = Cart.objects.get(id =pk)
        user_data = SkartUser.objects.get(user_id = userid)
        skartuserid = user_data.id 
        cart_data = Cart.objects.get(user_id = skartuserid)
        if pk_data != cart_data:
            raise NotAcceptable(detail="You are not authorized for this action.")
        existing_products = cart_data.products.all()
        existing_products_set = set(existing_products.values_list('pk', flat = True))
        existing_books = cart_data.books.all()
        existing_books_set = set(existing_books.values_list('pk', flat = True))
        request_products = request.data.get('products')
        request_books = request.data.get('books')
        if request_products is None:
            if existing_products_set is not None:
                request.data.update({'products':list(existing_products_set)})
        if existing_products_set is not None:
            whole_data_set = set(request.data['products']).union(existing_products_set)
            request.data['products'] = list(whole_data_set)

        if request_books is None:
            if existing_books_set is not None:
                request.data.update({'books':list(existing_books_set)})
        if existing_books_set is not None:
            whole_data_set = set(request.data['books']).union(existing_books_set)
            request.data['books'] = list(whole_data_set)

        return super().update(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        userid = self.request.user.id
        if pk is None:
            raise NotAcceptable(detail="No data provided.")
        pk_data = Cart.objects.get(id =pk)
        user_data = SkartUser.objects.get(user_id = userid)
        skartuserid = user_data.id 
        cart_data = Cart.objects.get(user_id = skartuserid)
        if pk_data != cart_data:
            raise NotAcceptable(detail="You are not authorized for this action.")
        return super().retrieve(request, *args, **kwargs)
    
    def get_queryset(self):
        return Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

class RemoveItemsCartView(generics.UpdateAPIView):
    #Removes the given products and books
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        userid = self.request.user.id
        pk = kwargs.get('pk')
        if pk is None:
            raise NotAcceptable(detail="Cart Id not provided.")
        pk_cart_data = Cart.objects.get(id = pk)
        skart_user_data = SkartUser.objects.get(user_id = userid)
        user_cart_data = Cart.objects.get(user_id = skart_user_data.id)
        if pk_cart_data != user_cart_data:
            raise NotAcceptable(detail="You are not authorized for this action.")
        existing_products = user_cart_data.products.all()
        existing_products_set = set(existing_products.values_list('pk', flat = True))
        requested_products = request.data.get('products')
        if requested_products is not None:
            if existing_products_set is None:
                request.data['products'] = None
            else:
                requested_products_set = set(requested_products)
                after_removing_products = existing_products_set.difference(requested_products_set)
                request.data['products'] = list(after_removing_products)
        else:
            if existing_products_set is not None:
                request.data.update({'products': list(existing_products_set)})
            else:
                pass
        existing_books = user_cart_data.books.all()
        existing_books_set = set(existing_books.values_list('pk', flat = True))
        requested_books = request.data.get('books')
        if requested_books is not None:
            if existing_books_set is None:
                request.data['books'] = None
            else:
                requested_books_set = set(requested_books)
                after_removing_books = existing_books_set.difference(requested_books_set)
                request.data['books'] = list(after_removing_books)
        else:
            if existing_books_set is not None:
                request.data.update({'books': list(existing_books_set)})
            else:
                pass
        
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        return Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]



class PlaceOrderView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        userid = self.request.user.id
        skart_user = SkartUser.objects.get(user_id = userid)
        cart_data = Cart.objects.get(user_id = skart_user.id)
        request.data['customer'] = skart_user.id
        cart_products = cart_data.products.all()
        request.data['products'] = list(cart_products.values_list('pk', flat = True))

        cart_books = cart_data.books.all()
        request.data['books'] = list(cart_books.values_list('pk', flat = True))
        request.data['total_price'] = cart_data.total_price
        return super().create(request, *args, **kwargs)
    queryset = PlaceOrder.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]