
from django.core import validators
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

Product_Catageory_Choices =[
    ('Clothes', (
        ('MW' ,"Men's wear"),
        ('WW', "Women's wear"),
        ('KW', "Kid's wear")
        )
    ),
    ('Shoes', (
        ('RS', "Running Shoes"),
        ('FS', "Formal Shoes"),
        ('SS', "sneakers"),
        ('BS', "Boots"),
        ('OS', "Others"),
        )
    ),
    ('Electronics', (
        ('LP', "Laptop"),
        ('M', "Mobile"),
        ('CP', "Computor Parts"),
        ('O', "Other"),
        )
    ),
    ('Stationery', (
        ('PS', "Pencils"),
        ('PN', "Pens"),
        ('CS', "Copies"),
        ('OT', "Other Stationeries"),
        )
    ),
    ('Electrics', (
        ('FE', "Fans"),
        ('CE', "Cables"),
        ('TE', " Thin wires"),
        ('LE', "LED"),
        ('TV', "Television"),
        ('BE', "Batteries"),
        ('OE', "Other Electric materials"),
        )
    ),
    ('Books',(
        ('Drama', 'Drama'),
        ('Self help books', 'Self help books'),
        ('Story books', 'Story Books'),
        ('Novels', 'Novels'),
        ('School books', 'School books'),
        ('Higher Education Books', 'Higher Education Books'),
        ('Other Books', 'Other Books'),
        )
    ),
    ('Other', "Other")
]


Order_status_choices = [
    ('Initialized', 'Initialized'),
    ('Dispatched', 'Dispatched'),
    ('OnRoute', 'On Route'),
    ('OutForDelivery', 'Out for delivery'),
    ('Delivered', 'Delivered'),
]


class ProductCategory(models.Model):
    product_category = models.CharField(max_length=255)
    def __str__(self):
        return self.product_category
class Seller(models.Model):
    seller = models.OneToOneField(User, on_delete=models.CASCADE)
    seller_name = models.CharField(max_length=255)
    store_address = models.TextField()
    mobile_number = models.IntegerField(validators=[MaxValueValidator(9999999999), MinValueValidator(1000000000)], unique = True)
    selling_product_category = models.ManyToManyField(ProductCategory, max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.seller_name
    def total_income(self):
        '''
        Total income will be the 90% of each sold product.
        '''
        total_income = 0
        seller_product_list = list(Product.objects.filter(seller_id = self.id))
        orders_list = list(PlaceOrder.objects.filter(order_status = 'Delivered'))
        for order in orders_list:
            product_orders_list = order.products.all()
            for product_order in product_orders_list:
                if product_order.product in seller_product_list:
                    total_income = total_income + product_order.order_price
        return total_income*0.90


class Product(models.Model):
    product_tag = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=255, choices= Product_Catageory_Choices)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='Product_seller')
    description = models.TextField(blank = True)
    additional_information = models.TextField(blank= True)
    image = models.ImageField(upload_to='uploads', null = True, blank = True)
    status = models.BooleanField(default= True)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']
    def __str__(self):
        return f'{self.product_tag} {self.name}'

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete= models.DO_NOTHING, related_name="ordered_products")
    quantity = models.PositiveSmallIntegerField(default=1)
    order_price = models.IntegerField(validators=[MinValueValidator(0)], blank= True, null=True)
    def __str__(self):
        return str(self.product.name) + str(self.id)




class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=False, blank=False)
    mobile_number = models.IntegerField(validators=[MaxValueValidator(9999999999), MinValueValidator(1000000000)], unique = True, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username
    

class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='customer')
    products = models.ManyToManyField(ProductOrder, blank=True, related_name='cart_products')
    updated_on = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-updated_on']
    def total_price(self):
        total_cart_price = 0
        for product in self.products.all():
            total_cart_price = total_cart_price + product.quantity*product.product.price
        return total_cart_price

class PlaceOrder(models.Model):
    order_status = models.CharField(max_length=255, choices=Order_status_choices, default='Initialized')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_order')
    products = models.ManyToManyField(ProductOrder, blank=True)
    receiver_name = models.CharField(max_length=255)
    receiver_mobile_number = models.IntegerField(validators=[MaxValueValidator(9999999999), MinValueValidator(1000000000)], blank=False)
    place = models.CharField(max_length=400)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    ordered_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-ordered_at']
    def total_price(self):
        total_cart_price = 0
        for product in self.products.all():
            total_cart_price = total_cart_price + product.quantity*product.product.price
        return total_cart_price
    def __str__(self):
        return str(self.customer)
    

class CancelledOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cancelled_customer')
    products = models.ManyToManyField(ProductOrder, blank=True)
    cancelled_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-cancelled_at']

