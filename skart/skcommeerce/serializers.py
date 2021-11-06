from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Book, Cart, Product,  SkartUser, PlaceOrder



class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'category', 'isbn', 'pages', 'price', 'stock', 'description','additional_information', 'image', 'status', 'date_created']
    

class ProducSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_tag', 'name', 'category', 'price', 'stock', 'description','additional_information', 'image', 'status', 'date_created']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        
        
        

class CreateSkartUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
   
    class Meta:
        model = SkartUser
        fields = ['user', 'mobile_number', 'date_of_birth', 'created_on', 'updated_on']
        

    def create(self, validated_data):
        user = validated_data.pop('user')
        user_instance = User.objects.create_user(**user)
        return SkartUser.objects.create(user = user_instance, **validated_data)



class UpdateSkartUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkartUser
        fields = ['user', 'mobile_number', 'date_of_birth', 'created_on', 'updated_on']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user', 'products', 'books', 'total_price', 'updated_on']
        # read_only_fields = ['total_price']

    def save(self):
        if self.validated_data.get('products') is not None:
            x=0
            for product in self.validated_data['products']:
                x = x + product.price
        else:
            x = 0
        
        if self.validated_data.get('books') is not None:
            y=0
            for book in self.validated_data['books']:
                y = y + book.price
        else:
            y = 0
        self.validated_data['total_price'] = x+y
        return super().save()


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceOrder
        fields = ['customer', 'products', 'books', 'total_price','receiver_name','receiver_name','receiver_mobile_number', 'place', 'district', 'state', 'country', 'ordered_at', 'updated_at']

class OrderedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceOrder
        fields = ['customer','order_status', 'products', 'books', 'total_price','receiver_name','receiver_name','receiver_mobile_number', 'place', 'district', 'state', 'country', 'ordered_at', 'updated_at']




  