from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import (Cart, Product,  Customer, PlaceOrder,
 CancelledOrder, ProductCategory, Seller, ProductOrder
)


    

class ProducSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'seller', 'product_tag', 'name', 'category', 'price', 'stock', 'description','additional_information', 'image', 'status', 'date_created']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        

        

class CreateCustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        fields = ['user', 'mobile_number', 'date_of_birth', 'created_on', 'updated_on']
    def create(self, validated_data):
        user = validated_data.pop('user')
        userinstance = User.objects.create(**user)
        return Customer.objects.create(user= userinstance, **validated_data)
        


class User2Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
    
class UpdateCustomerSerializer(serializers.ModelSerializer):
    user = User2Serializer()
    class Meta:
        model = Customer
        fields = ['user', 'mobile_number', 'date_of_birth', 'created_on', 'updated_on']
    def update(self, instance, validated_data):
        user_data = validated_data.get('user')
        if user_data is not None:
            instance.user.username = user_data.get('username', instance.user.username)
            instance.user.first_name = user_data.get('first_name', instance.user.first_name)
            instance.user.last_name = user_data.get('last_name', instance.user.last_name)
            instance.user.email = user_data.get('email', instance.user.email)
            instance.user.save()
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth) 
        instance.save()
        return instance

class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = ['product', 'quantity', 'order_price']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['customer', 'products', 'total_price', 'updated_on']
        
  
   


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceOrder
        fields = ['customer', 'order_status', 'products',  'total_price','receiver_name','receiver_name','receiver_mobile_number', 'place', 'district', 'state', 'country', 'ordered_at', 'updated_at']



class CancelledOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CancelledOrder
        fields = ['customer', 'products', 'cancelled_at']

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['product_category']
class SellerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'is_staff']
        extra_kwargs = {
            'is_staff': {'default' : True}
            }

class CreateSellerSerializer(serializers.ModelSerializer):
    seller = SellerUserSerializer()
    class Meta: 
        model = Seller
        fields = ['seller', 'seller_name', 'store_address', 'mobile_number', 'selling_product_category', 'created_at', 'updated_at']
    def create(self, validated_data):
        seller = validated_data.pop('seller')
        seller_instance = User.objects.create(**seller)
        validated_data.update({'seller':seller_instance})
        return super().create(validated_data)

class SellerUser2Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

class UpdateSellerSerializer(serializers.ModelSerializer):
    seller = SellerUser2Serializer
    class Meta:
        model = Seller
        fields = ['seller', 'seller_name', 'store_address', 'mobile_number', 'selling_product_category', 'created_at', 'updated_at']
    def update(self, instance, validated_data):  
        user_data = validated_data.get('seller')
        if user_data is not None:
            instance.seller.username = user_data.get('username', instance.seller.username)
            instance.seller.first_name = user_data.get('first_name', instance.seller.first_name)
            instance.seller.last_name = user_data.get('last_name', instance.seller.last_name)
            instance.seller.email = user_data.get('email', instance.seller.email)
            instance.seller.save()
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.seller_name = validated_data.get('seller_name', instance.seller_name) 
        seller_data = Seller.objects.get(id = instance.id)
        already_selling_category = seller_data.selling_product_category
        validated_category = validated_data.get('selling_product_category')
        
        if validated_category is None:
            raise ValidationError("No products provided to add in the cart.")
        else:
            if already_selling_category is None:
                instance.selling_product_category.set(validated_category, instance)
            else:
                already_selling_category_list = list(seller_data.selling_product_category.values_list('pk', flat = True))
                validated_category = list(set(validated_category).union(set(already_selling_category_list)))
                instance.selling_product_category.set(validated_category) 
        instance.store_address = validated_data.get('store_address', instance.store_address)
        instance.save()
        return instance






class RetrieveSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['seller', 'seller_name','total_income', 'store_address', 'mobile_number', 'selling_product_category', 'created_at', 'updated_at']


  