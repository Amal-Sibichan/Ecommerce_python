from django.contrib import admin

# Register your models here.
from django.contrib import admin
from.models import Userdetails
from.models import Address,Seller,Product,Image,Size,Category,Cart,Order








admin.site.register(Userdetails)
admin.site.register(Address)
admin.site.register(Seller)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Size)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order)