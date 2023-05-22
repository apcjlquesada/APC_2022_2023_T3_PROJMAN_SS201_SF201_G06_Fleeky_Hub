from django import forms
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.forms import UserCreationForm
from .models import region, province,barangay,city
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.utils.translation import gettext_lazy as _

class customerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class customerForm(forms.ModelForm):
    class Meta:
        model=models.customer
        fields=['region_text','province_text','barangay_text','city_text','zipcode','street','detailed_address','email','mobile','profile_pic','gender']    
        captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

class ProductForm(forms.ModelForm):
    class Meta:
        model =models.Product
        fields = ['name','price','fabric_type','set_type','qty','color','product_img','description','product_tag']
        
class MaterialsForm(forms.ModelForm):
    class Meta:
        model =models.materials
        fields = ['name','qty','unit','price','description']

class AnalyticsForm(forms.ModelForm):
    class Meta:
        model =models.analytics
        fields = ['fabric_type','payment','price','color','product_tag','set_tag','month_of_purhase','qty','count']

class addressForm(forms.Form):
    email = forms.EmailField()
    mobile = forms.IntegerField()
    region= forms.CharField()
    barangay = forms.CharField()
    zipcode = forms.IntegerField()
    street = forms.CharField()
    detailed_address = forms.CharField()
    
#for updating status of order
class OrderForm(forms.ModelForm):
    class Meta:
        model=models.Orders
        fields=['status']