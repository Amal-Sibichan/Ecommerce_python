
from django.db import models
from django.utils import timezone

class Userdetails(models.Model):
    firstname = models.CharField(max_length=30)
    phone = models.CharField(max_length=11)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

class Address(models.Model):
    email = models.ForeignKey(Userdetails, on_delete=models.CASCADE)
    home = models.CharField(max_length=55)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

class Seller(models.Model):
    id = models.AutoField(primary_key=True)
    seller_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=15)

class Size(models.Model):
    size_name = models.CharField(max_length=50)
   
   

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)


class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    discription = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    sizes = models.ManyToManyField(Size)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(default=timezone.now)
   
class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')


class Cart(models.Model):
    user= models.ForeignKey(Userdetails, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='cart_images/', null=True, blank=True)


class Order(models.Model):
    user = models.ForeignKey(Userdetails, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    status = models.CharField(max_length=30, default='Pending')
    pstatus = models.CharField(max_length=20)
    date = models.DateField(null=True, blank=True)
