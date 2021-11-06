from django.contrib import admin
from .models import  Book, Product, SkartUser, Cart, PlaceOrder, CancelledOrder
from django.contrib.auth.models import User
# Register your models here.


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'isbn', 'pages', 'price', 'stock', 'description','additional_information', 'image', 'status', 'date_created']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_tag', 'name', 'category', 'price', 'stock', 'description','additional_information', 'image', 'status', 'date_created']

@admin.register(SkartUser)
class SkartUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'user', 'mobile_number', 'date_of_birth', 'created_on', 'updated_on']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'cart_products', 'cart_books', 'updated_on']
    def cart_products(self, instance):
        return [product for product in instance.products.all()]
    def cart_books(self, instance):
        return [product for product in instance.books.all()]

@admin.register(PlaceOrder)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_status', 'customer', 'total_price','ordered_products', 'ordered_books','receiver_name','receiver_mobile_number', 'place', 'district', 'state', 'country' , 'ordered_at', 'updated_at']
    def ordered_products(self, instance):
        return [product for product in instance.products.all()]
    def ordered_books(self, instance):
        return [product for product in instance.books.all()]

@admin.register(CancelledOrder)
class CancelledOrdersAdmin(admin.ModelAdmin):
    list_display= ['id', 'customer', 'cancelled_products', 'cancelled_books', 'cancelled_at']
    def cancelled_products(self, instance):
        return [product for product in instance.products.all()]
    def cancelled_books(self, instance):
        return [product for product in instance.books.all()]
