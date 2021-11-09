
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics, status
import rest_framework
from rest_framework import request
from rest_framework.request import Request
from .serializers import (
    ProducSerializer, CreateCustomerSerializer, 
UpdateCustomerSerializer, CartSerializer, OrderSerializer, CancelledOrderSerializer,
CreateSellerSerializer, UpdateSellerSerializer, RetrieveSellerSerializer, ProductCategorySerializer, ProductOrderSerializer, UserSerializer
)
from .models import  (
    CancelledOrder, Customer, Product, Cart, PlaceOrder, Seller, ProductOrder, ProductCategory
)
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable, ValidationError
from .mypermissionclasses import IsSeller, IsCustomer



# Create your views here.


class ListProduct(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProducSerializer

class DetailProduct(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProducSerializer

class CreateCustomerView(generics.CreateAPIView):
    #request:
    '''
    {
        user:{first_name:  , last_name:   , email:  , username:  ,password1:  ,password2:  },
        mobile_number:  ,
        date_of_birth:  
    }
    This function create a customer with provided username and password and a cart related to the user with no products.
    '''
    def create(self, request, *args, **kwargs):
        if request.data is None:
            return NotAcceptable(detail="No data Provided")
        if request.data['user']['password1'] is None:
            return NotAcceptable(detail="Password1 is required.")
        if request.data['user']['password2'] is None:
            return NotAcceptable(detail="Password2 is required.")
        password1 = request.data['user']['password1']
        password2 = request.data['user']['password2']
        if password1 != password2:
            raise NotAcceptable(detail="Passwords did not match.")
        if len(str(password1)) < 8:
            raise NotAcceptable(detail= "Password must contain at least 8 characters")
        if password1.isdigit():
            raise NotAcceptable(detail="password must contain alphabets.")
        else:
            password1 = make_password(password1)
            request.data['user']['password'] = password1
            del password1
            del password2
            
            customer_serializer = CreateCustomerSerializer(data=request.data)
            customer_serializer.is_valid(raise_exception=True)
            customer_serializer.save()
            customer_instance = Customer.objects.get(mobile_number =request.data['mobile_number'])
            cart_serializer = CartSerializer(data={'customer':customer_instance.id, "products":[]})
            cart_serializer.is_valid(raise_exception=True)
            cart_serializer.save()

        return Response(f"Thank you very much for becoming our customer. Your details are:\n {customer_serializer.data}", status= status.HTTP_201_CREATED)

            
            
        
    

class CustomerProfile(generics.RetrieveUpdateDestroyAPIView):
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is None:
            raise NotAcceptable(detail="No data provided.")
        pk_data = Customer.objects.get(id = pk)
        user_data = Customer.objects.get(user_id = self.request.user.id)
        if pk_data != user_data:
            raise NotAcceptable(detail="You are not authorized for this data")
        return super().retrieve(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        pk = kwargs.get('pk')
        if pk is None:
            raise NotAcceptable(detail="No data provided.")
        pk_data = Customer.objects.get(id = pk)
        user_data = Customer.objects.get(user_id = self.request.user.id)
        if pk_data != user_data:
            raise NotAcceptable(detail="You are not authorized for this data")
        return super().update(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is None:
            raise NotAcceptable(detail="No data provided.")
        pk_data = Customer.objects.get(id = pk)
        user_data = Customer.objects.get(user_id = self.request.user.id)
        if pk_data != user_data:
            raise NotAcceptable(detail="You are not authorized for this data")
        return super().destroy(request, *args, **kwargs)
    def get_queryset(self):
        return Customer.objects.all().select_related('user')
    serializer_class = UpdateCustomerSerializer
    permission_classes = [IsCustomer]


class CreateSellerView(generics.CreateAPIView):
    #request:
    '''
    {
        seller:{email:  , username:  ,password1:  ,password2:  },
        mobile_number:  ,
        seller_name:    ,
        store_address:   ,
        selling_product_category:   
    }
    This function create a seller with provided username and password.
    '''
    def create(self, request, *args, **kwargs):
        if request.data is None:
            return NotAcceptable(detail="No data Provided")
        if request.data['seller']['password1'] is None:
            return NotAcceptable(detail="Password1 is required.")
        if request.data['seller']['password2'] is None:
            return NotAcceptable(detail="Password2 is required.")
        password1 = request.data['seller']['password1']
        password2 = request.data['seller']['password2']
        if password1 != password2:
            raise NotAcceptable(detail="Passwords did not match.")
        if len(str(password1)) < 8:
            raise NotAcceptable(detail= "Password must contain at least 8 characters")
        if password1.isdigit():
            raise NotAcceptable(detail="password must contain alphabets.")
        else:
            password1 = make_password(password1)
            request.data['seller']['password'] = password1
            del password1
            del password2
            request_user_data = request.data['seller']
            request_user_data.update({'is_staff':True})
        return super().create(request, *args, **kwargs)
    queryset = Seller.objects.all()
    serializer_class = CreateSellerSerializer
    
            
        
    

class SellerProfile(generics.RetrieveDestroyAPIView):
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is None:
            raise NotAcceptable(detail="No data provided.")
        pk_data = Seller.objects.get(id = pk)
        seller_data = Seller.objects.get(seller_id = self.request.user.id)
        if pk_data != seller_data:
            raise NotAcceptable(detail="You are not authorized for this data")
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is None:
            raise NotAcceptable(detail="No data provided.")
        pk_data = Seller.objects.get(id = pk)
        seller_data = Seller.objects.get(seller_id = self.request.user.id)
        if pk_data != seller_data:
            raise NotAcceptable(detail="You are not authorized for this data")
        return super().destroy(request, *args, **kwargs)
    def get_queryset(self):
        return Seller.objects.all().select_related('seller')
    serializer_class = RetrieveSellerSerializer
    permission_classes = [IsSeller]

class UpdateSellerProfile(generics.UpdateAPIView):
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        pk = kwargs.get('pk')
        if pk is None:
            raise NotAcceptable(detail="No data provided.")
        pk_data = Seller.objects.get(id = pk)
        seller_data = Seller.objects.get(seller_id = self.request.user.id)
        if pk_data != seller_data:
            raise NotAcceptable(detail="You are not authorized for this action.")
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        return Seller.objects.all().select_related('seller')
    serializer_class = UpdateSellerSerializer
    permission_classes = [IsSeller]




class CartUpdateView(generics.RetrieveUpdateAPIView):
    '''
    This view takes request as
    {
        'products':{
            'product':    ,
            'quantity':   ,
        }
    }
    And adds the given product in customer's cart with given quantity and updates it if it already exists.
    User can add one one by product to cart.
    '''
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        pk = kwargs.get('pk')
        if kwargs['pk'] is None:
            raise NotAcceptable(detail="Please provide cart id.")
        userid = self.request.user.id
        customer_data = Customer.objects.get(user_id = userid)
        card_data = Cart.objects.get(customer_id = customer_data.id)
        if pk != card_data.id:
            raise NotAcceptable(detail="You are not authorized for this action.")
        if request.data['products'] is None:
            raise NotAcceptable(detail="No product to add in the cart.")
        if request.data['products']['product'] is None:
            raise NotAcceptable(detail="No product to add in the cart.")
        if request.data['products']['quantity'] is None:
            request.data['products']['quantity'] = 1
        requested_productid = request.data['products']['product']
        requested_quantity = request.data['products']['quantity']
        if int(requested_quantity) < 1:
            raise NotAcceptable(detail="Please add at least one quantity.")
        requested_product = Product.objects.get(id = requested_productid)
        cart_products_list = card_data.products.all()
        cart_products_idlist = list(cart_products_list.values_list('pk', flat = True))
        if len(cart_products_idlist) != 0:
            for productthrough in cart_products_list:
                    if productthrough.product_id == int(requested_productid):
                        if max(int(requested_quantity), int(productthrough.quantity)) > productthrough.product.stock:
                            raise NotAcceptable(detail= "We don't have enough stock.")
                        added_product = ProductOrder.objects.get(product_id = requested_productid)
                        ProductOrder.objects.filter(product_id = int(requested_productid)).update(quantity = int(requested_quantity))
                        request.data['products'] = cart_products_idlist 
                        break
            else:
                if int(requested_quantity) > int(requested_product.stock):
                    raise NotAcceptable(detail= "We don't have enough stock.")
                productthrough_serializer = ProductOrderSerializer(data=request.data['products'])
                productthrough_serializer.is_valid(raise_exception=True)
                added_product = ProductOrder.objects.create(product = requested_product, quantity = int(requested_quantity))
                Response(added_product.quantity)
                updated_products_set = set(cart_products_idlist).union({added_product.id})
                request.data['products'] = list(updated_products_set)
                 
                    
        else:
            if int(request.data['products']['quantity']) > int(requested_product.stock):
                raise NotAcceptable(detail= "We don't have enough stock.")
            productthrough_serializer = ProductOrderSerializer(data=request.data['products'])
            productthrough_serializer.is_valid(raise_exception=True)
            added_product = ProductOrder.objects.create(product = requested_product, quantity = request.data['products']['quantity'])
            request.data['products'] = [added_product.id]
        return super().update(request, *args, **kwargs)
    
    def get_queryset(self):
        return Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsCustomer]

class CartRemoveView(generics.UpdateAPIView):
    '''
    This view takes request as
    {
        'products':{
            'product':    ,
            'quantity':   ,
        }
    }
    And updates the given product in customer's cart and decreases the quantity of product. If requested quantity exceeds or becomes equal to the quantity in cart, it removes that product from the cart.
    '''
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        pk = kwargs.get('pk')
        if kwargs['pk'] is None:
            raise NotAcceptable(detail="Please provide cart id.")
        userid = self.request.user.id
        customer_data = Customer.objects.get(user_id = userid)
        cart_data = Cart.objects.get(customer_id = customer_data.id)
        if pk != cart_data.id:
            raise NotAcceptable(detail="You are not authorized for this action.")
        if request.data['products'] is None:
            raise NotAcceptable(detail="No product to remove from the cart.")
        if request.data['products']['product'] is None:
            raise NotAcceptable(detail="No product to remove the cart.")
        requested_productid = request.data['products']['product']
        requested_quantity = request.data['products']['quantity']
        cart_products_list = cart_data.products.all()
        cart_products_idlist = list(cart_products_list.values_list('pk', flat = True))
        if len(cart_products_idlist) != 0:
            for productthrough in cart_products_list:
                if productthrough.product_id == int(requested_productid):
                    to_remove_product = cart_data.products.get(product_id = int(requested_productid))
                    if to_remove_product.quantity > int(requested_quantity):
                        cart_data.products.filter(product_id = int(requested_productid)).update(quantity =to_remove_product.quantity - int(requested_quantity))
                        request.data['products'] = cart_products_idlist
                    else:
                        request.data['products'] = list(set(cart_products_idlist).difference({to_remove_product.id}))
                        to_remove_product.delete() 
                    break
            else:
                raise NotAcceptable(detail="You don't have this item in your cart.")
                 
                    
        else:
            raise NotAcceptable(detail= "You don't have any itme in your cart.")
        return super().update(request, *args, **kwargs)
    
    def get_queryset(self):
        return Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsCustomer]



class PlaceOrderView(generics.ListCreateAPIView):
    '''
    This view places order of each item present in the cart and vacates the cart as well. The request data format is:
    {
    "receiver_name": "",
    "receiver_mobile_number": "",
    "place": "",
    "district": "",
    "state":"",
    "country": ""
    }
    '''
    def create(self, request, *args, **kwargs):
        userid = self.request.user.id
        customer = Customer.objects.get(user_id = userid)
        cart_data = Cart.objects.get(customer_id =  customer.id)
        cart_products = cart_data.products.all()
        if len(list(cart_products.values_list('pk', flat = True))) == 0:
            return Response("Please add at least one item in cart.", status=status.HTTP_406_NOT_ACCEPTABLE)
        if request.data is None:
            raise NotAcceptable(detail="No data provided.")
        if request.data.get('receiver_name') is None:
            raise NotAcceptable(detail='Receiver name not provided.')
        if request.data.get('receiver_mobile_number') is None:
            raise NotAcceptable(detail="Receiver's mobile number not provided.")
        if request.data.get('place') is None:
            raise NotAcceptable(detail='Place not provided.')
        if request.data.get('district') is None:
            raise NotAcceptable(detail='District name not provided.')
        if request.data.get('state') is None:
            raise NotAcceptable(detail='State name not provided.')
        if request.data.get('country') is None:
            raise NotAcceptable(detail='Country name not provided.')
        for product in list(cart_products):
            if product.quantity > product.product.stock:
                raise NotAcceptable(detail= f"This product {product.product.name} is currently out of stock.")
            else:
                ProductOrder.objects.filter(id = product.id).update(order_price = product.product.price*product.quantity)
                Product.objects.filter(id = product.product.id).update(stock = product.product.stock - product.quantity)
        request.data['customer'] = customer.id
        request.data['products'] = list(cart_products.values_list('pk', flat = True))
        none_list =[]
        cart_data.products.set(none_list)
        
        
        return super().create(request, *args, **kwargs)
    def get_queryset(self):
        customer = Customer.objects.get(user_id = self.request.user.id)
        return PlaceOrder.objects.filter(customer_id = customer.id)
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]




    
class ItemsCancelOrderView(generics.RetrieveUpdateAPIView):

    def update(self, request, *args, **kwargs):
        '''
        This update functions cancels orders of products one by one and list them in cancelled order. The input given as request is:
        {
            "products" : 'int'
        }
        If there remains no product in order after cancelletion, it deletes the order.
        '''
        kwargs['partial'] = True
        userid = self.request.user.id
        customer = Customer.objects.get(user_id = userid)
        pk = kwargs.get('pk')
        orderdatalist = list(PlaceOrder.objects.filter(customer_id = customer.id))
        orderdata = PlaceOrder.objects.get(id = pk)
        if orderdata not in orderdatalist:
            raise NotAcceptable(detail="You are not authorized for this action.")
        if request.data.get('products') is None:
            raise NotAcceptable(detail= "Please tell us which item to cancel.")
        ordered_products = orderdata.products.all()
        ordered_products_set = set(ordered_products.values_list('pk', flat=True))
        productid_to_be_cancelled = int(request.data.get('products'))
        if productid_to_be_cancelled not in ordered_products_set:
            raise NotAcceptable(detail="You have not ordered this product yet.")
        cancelled_order_data ={
            "customer": customer.id,
            "products": [productid_to_be_cancelled]
        }
        cancelled_order_serializer = CancelledOrderSerializer(data=cancelled_order_data)
        cancelled_order_serializer.is_valid(raise_exception=True)
        cancelled_order_serializer.save()
        request.data['customer']= customer.id
        remaining_products_set = ordered_products_set.difference({productid_to_be_cancelled})
        cancelled_product_order = ProductOrder.objects.get(id = productid_to_be_cancelled)
        Product.objects.filter(id = cancelled_product_order.product.id).update(stock = cancelled_product_order.product.stock+cancelled_product_order.quantity)
        if len(remaining_products_set) == 0:
            orderdata.delete()
            return Response("Your order has been cancelled.", status= status.HTTP_202_ACCEPTED)
        request.data.update({"products": list(remaining_products_set)})
        return super().update(request, *args, **kwargs)


    def retrieve(self, request, *args, **kwargs):
        '''
        This function retrieves the requested order.
        '''
        userid = self.request.user.id
        customer = Customer.objects.get(user_id = userid)
        pk = kwargs.get('pk')
        orderdata = PlaceOrder.objects.get(id = pk)
        userid = orderdata.customer_id
        if userid != customer.id:
            raise NotAcceptable(detail="You are not authorized for this action.")
        return super().retrieve(request, *args, **kwargs)
    queryset = PlaceOrder.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsCustomer]

class CancellOrderView(generics.ListCreateAPIView):
    def create(self, request, *args, **kwargs):
        '''
        This function cancels the whole order and lists it in cancelled orders.
        The request sent to it is:
        {
            "orderid": "int"
        }
        '''
        if request.data.get('orderid') is None:
            raise NotAcceptable(detail="Orderid is required.")
        order_id = int(request.data['orderid'])
        order_details = PlaceOrder.objects.get(id = order_id)
        custumorid = order_details.customer_id
        
        customer = Customer.objects.get(user_id = self.request.user.id)
        
        if custumorid != customer.id:
            raise NotAcceptable(detail= "You are not authorized to perform this action.")
        ordered_products = order_details.products.all()        
        request.data['products'] = list(ordered_products.values_list('pk', flat= True))
        request.data['customer']= customer.id
        for ordered_product in list(order_details.products.all()):
            Product.objects.filter(id = ordered_product.product.id).update(stock = ordered_product.product.stock + ordered_product.quantity)
        PlaceOrder.objects.filter(id = order_id).delete()
        return super().create(request, *args, **kwargs)
    def get_queryset(self):
        customer = Customer.objects.get(user_id = self.request.user.id)
        return CancelledOrder.objects.filter(customer_id = customer.id)
    serializer_class = CancelledOrderSerializer
    permission_classes = [IsCustomer]


class RetrieveCancelledOrderView(generics.RetrieveAPIView):
    '''
    This retrieves the requested cancelled order.
    '''
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        cancelled_orders_list = CancelledOrder.objects.get(id = pk)
        customerid = cancelled_orders_list.customer_id
        customer = Customer.objects.get(user_id = self.request.user.id)
        if customerid != customer.id:
            raise NotAcceptable(detail= "You are not authorized for this action.")
        return super().retrieve(request, *args, **kwargs)
    queryset = CancelledOrder.objects.all()
    serializer_class = CancelledOrderSerializer
    permission_classes= [IsCustomer]



'''
Now the upcoming views will deal with the listing and retrieving products by seller and retrieving of orders of their products.
'''

class ListCreateProductView(generics.ListCreateAPIView):
    '''
    Seller can get products list created by him and create new products too.
    '''
    def create(self, request, *args, **kwargs):
        userid = self.request.user.id
        seller = Seller.objects.get(seller_id = userid)
        request.data.update({'seller': seller.id})
        return super().create(request, *args, **kwargs)
    def get_queryset(self):
        userid = self.request.user.id
        seller = Seller.objects.get(seller_id = userid)
        return Product.objects.filter(seller = seller).select_related('seller')
    serializer_class = ProducSerializer
    permission_classes = [IsSeller]

class RetrieveUpdateDestroyProductsView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Seller can retrieve, update and destroy the products added by him.
    '''
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        userid = self.request.user.id
        seller = Seller.objects.get(seller_id = userid)
        return Product.objects.filter(seller = seller).select_related('seller')
    serializer_class = ProducSerializer
    permission_classes = [IsSeller]


