from django.db import models
from django.contrib.auth.models import User
from django.utils.dates import MONTHS
# Create your models here.

#LOCATIONS DATABASE

from django.utils.translation import gettext_lazy as _


class region(models.Model):
    psgcCode = models.IntegerField(_("psgcCode"),null=True, blank=True)
    regDesc = models.CharField(_("regDesc"),max_length=255, null=True, blank=True)
    regCode = models.IntegerField(_("regCode"),null=True, blank=True)
    
class province(models.Model):
    psgcCode = models.IntegerField(_("psgcCode"),null=True, blank=True)
    provDesc = models.CharField(_("provDesc"),max_length=255, null=True, blank=True)
    regCode = models.ForeignKey(region,on_delete=models.CASCADE)
    provCode = models.IntegerField(_("provCode"),null=True, blank=True)

class city(models.Model):
    psgcCode = models.IntegerField(_("psgcCode"),null=True, blank=True)
    citymunDesc = models.CharField(_("citymunDesc"),max_length=255, null=True, blank=True)
    regDesc = models.IntegerField(_("regDesc"),null=True, blank=True)
    provCode = models.ForeignKey(province,on_delete=models.CASCADE)
    citymunCode = models.IntegerField(_("citymunCode"),null=True, blank=True)
    
class barangay(models.Model):
    brgyCode = models.IntegerField(_("brgyCod"),null=True, blank=True)
    brgyDesc = models.CharField(_("brgyDesc"),max_length=255, null=True, blank=True)
    regCode = models.IntegerField(_("regCode"),null=True, blank=True)
    provCode = models.IntegerField(_("provCode"),null=True, blank=True)
    citymunCode = models.ForeignKey(city,on_delete=models.CASCADE)

#==========================================================BREAKER==========================================
#Customer Model
class customer(models.Model):
    GENDER_CHOICES = (
        (1, 'male'),
        (2, 'female'),
        (3, 'other')
    )
   
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    email = models.EmailField(max_length=50,null=True)
    profile_pic =models.ImageField(upload_to='fchub/static/profile_pic/customer_profile_pic',null=True,default='fchub/static/profile_pic/customer_profile_pic/akbay.png')
    gender =  models.SmallIntegerField(choices=GENDER_CHOICES)
    mobile = models.CharField(max_length=20,null=True)
    
    region_text =models.CharField(max_length=250,null=True)
    province_text =models.CharField(max_length=250,null=True)
    barangay_text =models.CharField(max_length=250,null=True)
    city_text =models.CharField(max_length=250,null=True)
    
    zipcode = models.PositiveIntegerField()
    street = models.CharField(max_length=250,null=True)
    detailed_address=models.CharField(max_length=250,null=True)
    
    @property
    def get_name(self):
          return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name

#==========================================================BREAKER==========================================
#PRODUCT MODEL
class Product(models.Model):
    
    PRODUCT_TAG_CHOICES = (
        (1, 'Blockout'),
        (2, '5-in-1 Katrina'),
        (3, '3-in-1 Katrina'),
        (4, 'Tieback Holder'),
    )

    name=models.CharField(max_length=250)
    product_img = models.ImageField(upload_to='fchub/static/product_img/product_pic',null=True,blank=True)
    price = models.PositiveIntegerField()
    fabric_type=models.CharField(max_length=250)
    set_type = models.CharField(max_length=250)
    qty = models.PositiveIntegerField()
    color = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    product_tag = models.SmallIntegerField(choices=PRODUCT_TAG_CHOICES)
    def __str__(self):
        return self.name
    
class materials(models.Model):
    name = models.CharField(max_length=250)
    qty = models.CharField(max_length=250)
    unit = models.CharField(max_length=250)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=250,null=True)
    def __str__(self):
        return self.name
#==========================================================BREAKER==========================================

class Orders(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    customer=models.ForeignKey('customer', on_delete=models.CASCADE,null=True)
    product=models.ForeignKey('product',on_delete=models.CASCADE,null=True)
    email = models.CharField(max_length=50,null=True)
    region =models.CharField(max_length=250,null=True)
    province =models.CharField(max_length=250,null=True)
    barangay =models.CharField(max_length=250,null=True)
    city =models.CharField(max_length=250,null=True)
    zipcode = models.PositiveIntegerField(null=True)
    street = models.CharField(max_length=250,null=True)
    detailed_address = models.CharField(max_length=250,null=True)
    mobile = models.CharField(max_length=250,null=True)
    order_date= models.DateField(auto_now_add=True,null=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS)
    
    def __str__(self):
        return self.customer

class analytics(models.Model):
    
    PAYMENT_CHOICES = (
        ('GCASH','GCASH'),
        ('CASH ON DELIVERY','CASH ON DELIVERY'),
        ('LBC','LBC'),
        ('OTHERS','OTHERS'),
    )
    PRODUCT_TAG_CHOICES = (
        (1, 'Blockout'),
        (2, '5-in-1 Katrina'),
        (3, '3-in-1 Katrina'),
        (4, 'Tieback Holder'),
    )
    FABRIC_CHOICES = (
        ('Katrina','Katrina'),
        ('Blockout','Blockout'),
        ('Sheer','Sheer'),
        ('None','None'),
    )
    
    SET_CHOICES = (
        ('5-in-1','5-in-1'),
        ('3-in-1','3-in-1'),
        ('Single','Single'),
        ('None','None'),
    )
    fabric_type = models.CharField(max_length=250, null= True,choices=FABRIC_CHOICES)
    payment = models.CharField(max_length=250,null=True,choices=PAYMENT_CHOICES)
    price  = models.PositiveIntegerField(null=True)
    color = models.CharField(max_length=250, null=True)
    product_tag = models.SmallIntegerField(choices=PRODUCT_TAG_CHOICES)
    set_tag = models.CharField(max_length=250, choices=SET_CHOICES, null=True)
    month_of_purhase = models.PositiveSmallIntegerField(null=True,choices=MONTHS.items())
    qty = models.PositiveIntegerField(null=True)
    count = models.PositiveIntegerField(null=True)
    