from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Book, Product,  SkartUser



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
    # new_password = serializers.CharField()
    # confirm_password = serializers.CharField()
    class Meta:
        model = SkartUser
        fields = ['user', 'mobile_number', 'date_of_birth', 'created_on', 'updated_on']
        # write_only_fields = ['new_password', 'confirm_password']

    def create(self, validated_data):
        user = validated_data.pop('user')
        user_instance = User.objects.create_user(**user)
        return SkartUser.objects.create(user = user_instance, **validated_data)


class UpdateSkartUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['user', 'mobile_number', 'date_of_birth', 'created_on', 'updated_on']