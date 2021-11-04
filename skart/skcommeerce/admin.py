from django.contrib import admin
from .models import  Book, Product, SkartUser
from django.contrib.auth.models import User
# Register your models here.


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'isbn', 'pages', 'price', 'stock', 'description','additional_information', 'image', 'status', 'date_created']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_tag', 'name', 'category', 'price', 'stock', 'description','additional_information', 'image', 'status', 'date_created']

@admin.register(SkartUser)
class SkartUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'mobile_number', 'date_of_birth', 'created_on', 'updated_on']

