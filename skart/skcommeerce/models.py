from django.core import validators
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

Product_Catageory_Choices =[
    ('Clothes', (
        ('MW' ,"Men's wear"),
        ('WW', "Women's wear"),
        ('CD', "Kid's wear")
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
        ('CM', "Computor Parts"),
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
    ('Other', "Other")
]

Book_Category_Choices = [
    ('Drama', 'Drama'),
    ('Self help books', 'Self help books'),
    ('Story books', 'Story Books'),
    ('Novels', 'Novels'),
    ('School books', 'School books'),
    ('Higher Education Books', 'Higher Education Books'),
    ('Other Books', 'Other Books'),
]

Order_status_choices = [
    ('Initialized', 'initialized'),
    ('Dispatched', 'Dispatched'),
    ('On Route', 'On Route'),
    ('Out for delivery', 'Out for delivery'),
    ('Delivered', 'Delivered'),
]

class Book(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=200, choices=Book_Category_Choices)
    isbn = models.CharField(max_length=20)
    pages = models.IntegerField()
    price = models.IntegerField(validators=[MinValueValidator(0)])
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.TextField(blank= True)
    additional_information = models.TextField(blank= True)
    image = models.ImageField(upload_to='uploads', null = True, blank = True)
    status = models.BooleanField(default= True)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']
    def __str__(self):
        return self.title

class Product(models.Model):
    product_tag = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=255, choices= Product_Catageory_Choices)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.TextField(blank = True)
    additional_information = models.TextField(blank= True)
    image = models.ImageField(upload_to='uploads', null = True, blank = True)
    status = models.BooleanField(default= True)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']
    def __str__(self):
        return f'{self.product_tag} {self.name}'

class SkartUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=False, blank=False)
    mobile_number = models.IntegerField(validators=[MaxValueValidator(9999999999), MinValueValidator(1000000000)], unique = True, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    

class Cart(models.Model):
    user = models.OneToOneField(SkartUser, on_delete=models.CASCADE, related_name='customer')
    products = models.ManyToManyField(Product, blank=True)
    books = models.ManyToManyField(Book, blank= True)
    total_price = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)

class PlaceOrder(models.Model):
    order_status = models.CharField(max_length=255, choices=Order_status_choices)
    customer = models.ForeignKey(SkartUser, on_delete=models.CASCADE, related_name='customer_order')
    products = models.ManyToManyField(Product, blank=True)
    books = models.ManyToManyField(Book, blank= True)
    total_price = models.IntegerField(default=0)
    receiver_name = models.CharField(max_length=255)
    receiver_mobile_number = models.IntegerField(validators=[MaxValueValidator(9999999999), MinValueValidator(1000000000)], blank=False)
    place = models.CharField(max_length=400)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    ordered_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)

class CancelledOrder(models.Model):
    customer = models.ForeignKey(SkartUser, on_delete=models.CASCADE, related_name='cancelled_customer')
    products = models.ManyToManyField(Product, blank=True)
    books = models.ManyToManyField(Book, blank= True)
    cancelled_at = models.DateTimeField(auto_now_add=True)
    