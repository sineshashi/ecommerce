from django.contrib import admin
from .models import  (
     Product, Customer, Cart, PlaceOrder, CancelledOrder,
ProductCategory, Seller, ProductOrder
)
from django.contrib.auth.models import User
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'seller_id', 'product_tag', 'name', 'category', 'price', 'stock', 'seller_name', 'description','additional_information', 'image', 'status', 'date_created']
    def seller_name(self, instance):
        return instance.seller.seller_name

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'user', 'mobile_number', 'date_of_birth', 'created_on', 'updated_on']

@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'quantity', 'order_price']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_username','customer_name', 'total_price', 'cart_products',  'updated_on']
    def cart_products(self, instance):
        return [f"{product.id} {product.product.name}(quantity = {product.quantity}, id = {product.id})" for product in instance.products.all()]
    def customer_username(self, instance):
        return f"{instance.customer.user.username}"
    def customer_name(slef, instance):
        return f"{instance.customer.user.first_name} {instance.customer.user.last_name}"
    


@admin.register(PlaceOrder)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_status', 'customer_id', 'customer_username', 'total_price','ordered_products', 'receiver_name','receiver_mobile_number', 'place', 'district', 'state', 'country' , 'ordered_at', 'updated_at']
    def ordered_products(self, instance):
        return [f"{product.id} {product.product.name}({product.quantity})" for product in instance.products.all()]
    def customer_username(self, instance):
        return instance.customer.user.username

@admin.register(CancelledOrder)
class CancelledOrdersAdmin(admin.ModelAdmin):
    list_display= ['id', 'customer_username', 'cancelled_products', 'cancelled_at']
    def cancelled_products(self, instance):
        return [f"{product.id} {product.product.name}({product.quantity})" for product in instance.products.all()]
    def customer_username(self, instance):
        return instance.customer.user.username

    
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_category']
    
@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display= ['id', 'seller_id', 'seller_name', 'total_income', 'store_address', 'mobile_number', 'product_categories', 'created_at', 'updated_at']
    def product_categories(self, instance):
        return [product.product_category for product in instance.selling_product_category.all()]



