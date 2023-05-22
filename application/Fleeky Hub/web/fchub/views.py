from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.conf import settings
from django.views.generic import TemplateView
from django.conf import settings
from django.core.mail import send_mail
from . import models


def home_view(request):
    products=models.Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'index.html',{'Products':products,'product_count_in_cart':product_count_in_cart})
    

    
def products_view(request):
    products=models.Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'products.html',{'Products':products,'product_count_in_cart':product_count_in_cart})

@login_required(login_url="customerLogin")
def customer_products_view(request):
    products=models.Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'customer-products.html',{'Products':products,'product_count_in_cart':product_count_in_cart})



#for showing login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')

    

def customer_signup_view(request):
    userForm=forms.customerUserForm(request.POST or None)
    customerForm=forms.customerForm(request.POST or None)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.customerUserForm(request.POST)
        customerForm=forms.customerForm(request.POST,request.FILES)
        #print(userForm.is_valid() and customerForm.is_valid())
        #print(userForm.is_valid())
        #print(customerForm.is_valid())  
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            """ 
            data = customerForm.cleaned_data
            region = models.region.objects.filter(regCode=customerForm.cleaned_data['province']).values_list('regode','regDesc')
            regionWord =""
            for x in region:
                if data['region'] == x['regCode']:
                    regionWord = x['regDesc']
                    customer.province = regionWord
            print(data)
            """
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            username = request.POST['username']
            mobile = request.POST['mobile']
            email = request.POST['email']
            region = request.POST['region_text']
            province = request.POST['province_text']
            city = request.POST['city_text']
            barangay = request.POST['barangay_text']
            street = request.POST['street']
            zipcode = request.POST['zipcode']
            subject = (" Welcome to Fleeky Hub! ") 
            message = "Thank you for registering to our website! \n" 
            
            #update_region = customerForm.changed_data.append(region)
    
            print(region)
            print(city)
            print(province)
            print(barangay)
            
            send_mail(
                subject,
                message + '\n' + 
                'Hello! ' +' '+ username +','+ '\n\n' 
                + 'You created an account on our website Fleeky Hub Feel Free to browse on our shop!' +
                'Thank you for signing up in Fleeky Hub! We are excited to have you on board and look forward to providing you with a great experience.\n \n' +
                'Your account has been created successfully, and you can now log in using your username and password. Once logged in, you can explore the platform, browse our content, and interact with other users.\n \n'
                +'If you have any questions or need assistance, please feel free to reach out to our customer support team at development.fleekyhub@gmail.com. We are always here to help. \n\n'
                +'Thank you again for choosing our platform. We appreciate your trust in us and are committed to providing you with the best possible service.\n\n'
                +'-------------------------\n' + 'Your Info\n' +'-------------------------\n'
                + 'Full Name: ' + firstname + ' ' + lastname + '\n'
                + 'Email: ' + email + '\n' 
                + 'Contact Number: ' + mobile + '\n'
                +'-------------------------\n' + 'Your Info\n' +'-------------------------\n'
                + '\n\n'
                +'You can check our social media here: \n'
                +'Facebook: fb.com/fleekycurtainsph\n'
                +'Instagram: @fleekycurtainsph\n'
                +'Google: fleekycurtains@gmail.com'
                ,
                'settings.EMAIL_HOST_USER',
                [email],
                fail_silently=False
            )
            send_mail(
                'New User Account Created!',
                'User Info ' + '\n'
                +'Username: '+ username + '\n'
                +'Full Name: ' + firstname + ' ' + lastname + '\n'
                +'Email: ' + email + '\n'
                +'Contact Number: ' + mobile + '\n' 
                +'Address: ' + street +', ' + city + ' '+ barangay + ', ' + region + ' '  + province + ', ' + zipcode + ' '
                ,
                'settings.EMAIL_HOST_USER',
                ['development.fleekyhub@gmail.com'],
                fail_silently=False
            )
            
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
            return HttpResponseRedirect('customerlogin')
    return render(request,'customersignup.html',context=mydict)

#-----------for checking user iscustomer
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,CUSTOMER
def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('customer-home')
    else:
        return redirect('admin-dashboard')

#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    # for cards on dashboard
    customercount=models.customer.objects.all().count()
    productcount=models.Product.objects.all().count()
    ordercount=models.Orders.objects.all().count()

    # for recent order tables
    orders=models.Orders.objects.all()
    ordered_products=[]
    ordered_bys=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_by=models.customer.objects.all().filter(id = order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)

    mydict={
    'customercount':customercount,
    'productcount':productcount,
    'ordercount':ordercount,
    'data':zip(ordered_products,ordered_bys,orders),
    }
    return render(request,'admin-dashboard.html',context=mydict)


# admin view customer table
@login_required(login_url='adminlogin')
def view_customer_view(request):
    customers=models.customer.objects.all()
    return render(request,'view-customer.html',{'customers':customers})

# admin delete customer
@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=models.customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('view-customer')


@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=models.customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.customerUserForm(instance=user)
    customerForm=forms.customerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.customerUserForm(request.POST,instance=user)
        customerForm=forms.customerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('view-customer')
    return render(request,'admin-update-customer.html',context=mydict)

# admin view the product
@login_required(login_url='adminlogin')
def admin_products_view(request):
    products=models.Product.objects.all()
    return render(request,'admin-products.html',{'Products':products})


# admin add product by clicking on floating button
@login_required(login_url='adminlogin')
def admin_add_product_view(request):
    productForm=forms.ProductForm()
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
        return HttpResponseRedirect('admin-products')
    return render(request,'admin-add-products.html',{'ProductForm':productForm})

# admin view the product
@login_required(login_url='adminlogin')
def admin_materials_view(request):
    materials=models.materials.objects.all()
    return render(request,'admin-materials.html',{'Materials':materials})


# admin add product by clicking on floating button
@login_required(login_url='adminlogin')
def admin_add_materials_view(request):
    materialsForm=forms.MaterialsForm()
    if request.method=='POST':
        materialsForm=forms.MaterialsForm(request.POST, request.FILES)
        if materialsForm.is_valid():
            materialsForm.save()
        return HttpResponseRedirect('admin-materials')
    return render(request,'admin-add-materials.html',{'MaterialsForm':materialsForm})

@login_required(login_url='adminlogin')
def delete_product_view(request,pk):
    product=models.Product.objects.get(id=pk)
    product.delete()
    return redirect('admin-products')


@login_required(login_url='adminlogin')
def update_product_view(request,pk):
    Product=models.Product.objects.get(id=pk)
    ProductForm=forms.ProductForm(instance=Product)
    if request.method=='POST':
        ProductForm=forms.ProductForm(request.POST,request.FILES,instance=Product)
        if ProductForm.is_valid():
            ProductForm.save()
            return redirect('admin-products')
    return render(request,'admin-update-product.html',{'ProductForm':ProductForm})

@login_required(login_url='adminlogin')
def delete_materials_view(request,pk):
    materials=models.materials.objects.get(id=pk)
    materials.delete()
    return redirect('admin-materials')


@login_required(login_url='adminlogin')
def update_materials_view(request,pk):
    materials=models.materials.objects.get(id=pk)
    MaterialsForm=forms.MaterialsForm(instance=materials)
    if request.method=='POST':
        MaterialsForm=forms.MaterialsForm(request.POST,request.FILES,instance=materials)
        if MaterialsForm.is_valid():
            MaterialsForm.save()
            return redirect('admin-materials')
    return render(request,'admin-update-materials.html',{'MaterialsForm':MaterialsForm})


@login_required(login_url='adminlogin')
def admin_view_booking_view(request):
    orders=models.Orders.objects.all()
    ordered_products=[]
    ordered_bys=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_by=models.customer.objects.all().filter(id = order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)
    return render(request,'admin-view-booking.html',{'data':zip(ordered_products,ordered_bys,orders)})


@login_required(login_url='adminlogin')
def delete_order_view(request,pk):
    order=models.Orders.objects.get(id=pk)
    order.delete()
    return redirect('admin-view-booking')

# for changing status of order (pending,delivered...)
@login_required(login_url='adminlogin')
def update_order_view(request,pk):
    order=models.Orders.objects.get(id=pk)
    orderForm=forms.OrderForm(instance=order)
    email = customer.email
    
    if request.method=='POST':
        orderForm=forms.OrderForm(request.POST,instance=order)
        if orderForm.is_valid():
            #pending = orderForm.cleaned_data['Pending']
            #OC = orderForm.cleaned_data['Order Confirmed']
            #OD = orderForm.cleaned_data['Out for Delivery']
            #DE = orderForm.cleaned_data['Delivered']
            orderForm.save()
            return redirect('admin-view-booking')
        
        send_mail(
            'We have received your order!'
            ,
            'Your Order Now is being processed feel free to send us feedback'
            ,
            'settings.EMAIL_HOST_USER'
            ,
            ['development.fleekyhub@gmail.com']
            )
    return render(request,'update-order.html',{'orderForm':orderForm})


#---------------------------------------------------------------------------------
#------------------------ PUBLIC CUSTOMER RELATED VIEWS START ---------------------
#---------------------------------------------------------------------------------
def search_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    products=models.Product.objects.all().filter(name__icontains=query)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Searched Result :"

    if request.user.is_authenticated:
        return render(request,'customer-home.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart, 'search_text': query})
    return render(request,'index.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart, 'search_text': query})


# any one can add product to cart, no need of signin
def add_to_cart_view(request,pk):
    products=models.Product.objects.all()

    #for cart counter, fetching products ids added by customer from cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=1

    response = render(request, 'cart.html',{'Products':products,'product_count_in_cart':product_count_in_cart,'redirect_to' : request.GET['next_page']})

    #adding product id to cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids=="":
            product_ids=str(pk)
        else:
            product_ids=str(product_ids)+"|"+str(pk)
        response.set_cookie('product_ids', product_ids)
        
    else:
        product_ids = pk
        response.set_cookie('product_ids', pk)
  

    product=models.Product.objects.get(id=pk)
    messages.info(request, product.name + ' added to cart successfully!')

    return response



# for checkout of cart
def cart_view(request):
    #for cart counter
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # fetching product details from db whose id is present in cookie
    products=None
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_id_in_cart=product_ids.split('|')
            products=models.Product.objects.all().filter(id__in = product_id_in_cart)

            #for total price shown in cart
            for p in products:
                total=total+p.price
    return render(request,'cart.html',{'Products':products,'total':total,'product_count_in_cart':product_count_in_cart})


def remove_from_cart_view(request,pk):
    #for counter in cart
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # removing product id from cookie
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        product_id_in_cart=product_ids.split('|')
        product_id_in_cart=list(set(product_id_in_cart))
        product_id_in_cart.remove(str(pk))
        products=models.Product.objects.all().filter(id__in = product_id_in_cart)
        #for total price shown in cart after removing product
        for p in products:
            total=total+p.price

        #  for update coookie value after removing product id in cart
        value=""
        for i in range(len(product_id_in_cart)):
            if i==0:
                value=value+product_id_in_cart[0]
            else:
                value=value+"|"+product_id_in_cart[i]
        response = render(request, 'cart.html',{'products':products,'total':total,'product_count_in_cart':product_count_in_cart,'redirect_to' : request.GET['next_page']})
        if value=="":
            response.delete_cookie('product_ids')
        response.set_cookie('product_ids',value)
        return response


#--------------------------------------------------------------------------------
#------------------------ CUSTOMER RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_home_view(request):
    products=models.Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    return render(request,'customer-home.html',{'Products':products,'product_count_in_cart':product_count_in_cart})



# shipment address before placing order
@login_required(login_url='customerlogin')
def customer_address_view(request):
    user = models.User.objects.all()
    customer = models.customer.objects.get(user_id=request.user.id)
    orders = models.Orders.objects.all()
    # this is for checking whether product is present in cart or not
    # if there is no product in cart we will not show address form
    product_in_cart=False
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_in_cart=True
    #for counter in cart
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
       #for cart counter
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    # fetching product details from db whose id is present in cookie
    products=None
    total=0
    vat = 0.12
    f_region=customer.region_text
    three = ["National Capital Region (NCR)","Region I (Ilocos Region)","Region II (Cagayan Valley)","Region III (Central Luzon)","Region IV-A (CALABARZON)","Region V (Bicol Region)"]
    four = ["Region VI (Western Visayas)","Region VII (Central Visayas)","Region VIII (Eastern Visayas)"]
    five = ["Region IX (Zamboanga Peninzula)","Region X (Northern Mindanao)","Region XI (Davao Region)","Region XII (SOCCSKSARGEN)","Region XIII (Caraga)","Cordillera Administrative Region (CAR)","Autonomous Region in Muslim Mindanao (ARMM)"]
    print(f_region)
    sf_three = 300
    sf_four = 400
    sf_five = 500
    shipping_fee = 0
    total_price = 0
    if 'product_ids' in request.COOKIES:
                product_ids = request.COOKIES['product_ids']
                if product_ids != "":
                    product_id_in_cart=product_ids.split('|')
                    products=models.Product.objects.all().filter(id__in = product_id_in_cart)

            #for total price shown in cart
                    for p in products:
                        total=total+p.price
                        tmp = total*vat
                        with_vat = total+tmp 
                        for i in three:
                            if i == f_region:
                                total_price = with_vat+sf_three
                                shipping_fee = sf_three
                                print("three",total_price)
                        for i in four:
                            if i == f_region:
                                total_price = with_vat+sf_four
                                shipping_fee = sf_four
                                print("four", total_price)
                        for i in five:
                            if i == f_region:
                                total_price = with_vat+sf_five
                                shipping_fee = sf_five
                                print("five", total_price)
    return render(request,'customer-address.html',{'shipping_fee':shipping_fee,'total_price':total_price,'vat':vat,'with_vat':with_vat,'Products':products,'total':total,'orders':orders,'user':user,'product_in_cart':product_in_cart,'product_count_in_cart':product_count_in_cart, 'customer':customer})

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def payment(request):
    user = models.User.objects.all()
    customer = models.customer.objects.get(user_id=request.user.id)
    orders = models.Orders.objects.all()
    # this is for checking whether product is present in cart or not
    # if there is no product in cart we will not show address form
    product_in_cart=False
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_in_cart=True
    #for counter in cart
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
       #for cart counter
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    # fetching product details from db whose id is present in cookie
    products=None
    total=0
    vat = 0.12
    f_region=customer.region_text
    three = ["National Capital Region (NCR)","Region I (Ilocos Region)","Region II (Cagayan Valley)","Region III (Central Luzon)","Region IV-A (CALABARZON)","Region V (Bicol Region)"]
    four = ["Region VI (Western Visayas)","Region VII (Central Visayas)","Region VIII (Eastern Visayas)"]
    five = ["Region IX (Zamboanga Peninzula)","Region X (Northern Mindanao)","Region XI (Davao Region)","Region XII (SOCCSKSARGEN)","Region XIII (Caraga)","Cordillera Administrative Region (CAR)","Autonomous Region in Muslim Mindanao (ARMM)"]
    print(f_region)
    sf_three = 300
    sf_four = 400
    sf_five = 500
    shipping_fee = 0
    total_price = 0
    
    if 'product_ids' in request.COOKIES:
                product_ids = request.COOKIES['product_ids']
                if product_ids != "":
                    product_id_in_cart=product_ids.split('|')
                    products=models.Product.objects.all().filter(id__in = product_id_in_cart)
            #for total price shown in cart
                    for p in products:
                        total=total+p.price
                        tmp = total*vat
                        with_vat = total+tmp 
                        for i in three:
                            if i == f_region:
                                total_price = with_vat+sf_three
                                shipping_fee = sf_three
                                print("three",total_price)
                        for i in four:
                            if i == f_region:
                                total_price = with_vat+sf_four
                                shipping_fee = sf_four
                                print("four", total_price)
                        for i in five:
                            if i == f_region:
                                total_price = with_vat+sf_five
                                shipping_fee = sf_five
                                print("five", total_price)
                        
    c_email =customer.user.email  
    firstname = customer.user.first_name
    lastname = customer.user.last_name
    street = customer.street
    barangay = customer.barangay_text
    region = customer.region_text
    province = customer.province_text
    zipcode = str(customer.zipcode)
    total_orders = str(product_count_in_cart) 
    totalPrice = str(with_vat)
    #email to admin
    send_mail( 
            'New Pending Order!',
            'User Info ' + '\n'
            +'Full Name: '+ firstname + ' ' + lastname +'\n'
            +'Products Orders: ' + total_orders + '\n' 
            + 'Email: ' + '\n'
            +'Address :' + street + ' '+ barangay + ' , ' + region + ' ' + province + zipcode            
            + '\n'+'Total Order: ' + totalPrice + ' '
            ,
            'settings.EMAIL_HOST_USER',
            ['development.fleekyhub@gmail.com'],
            fail_silently=False
            )
    #email to customer
    #send_mail(
    #    'Woo hoo! We received your Order!'
    #    ,
    #    'Hey !' + firstname + ' ' + lastname + ' ! ' + '\n'
    #   +'\n' + 'We just wanted to drop you a quick note to say thank you for placing an order with us! We are super excited to be able to send you your goodies! '  '\n'      
    #   +'\n' + 'Your order is being processed. If you have any questions or concerns, please don''t hesitate to reach out to our customer support team at fleekycurtains@gmail.com. We''re always here to help and answer any of your questions.''\n'
    #   +'\n' + 'We appreciate your business and look forward to providing you with the best experience possible.' '\n'
    #   +'\n' + 'Thanks again for choosing us. Get ready to enjoy your new purchase!' '\n'
    #   +'\n' + 'Cheers,' + '\n' + 'Pallas Fontiveros' 
    #    ,
    #    'settings.EMAIL_HOST_USER'
    #    ,
    #    [c_email,'development.fleekyhub@gmail.com'],
    #    fail_silently = False
    #)
    
    return render(request,'payment.html',{'total_price':total_price,'shipping_fee':shipping_fee,'with_vat':with_vat,'Products':products,'total':total,'orders':orders,'user':user,'product_in_cart':product_in_cart,'product_count_in_cart':product_count_in_cart, 'customer':customer})
    


# here we are just directing to this view...actually we have to check whther payment is successful or not
#then only this view should be accessed
@login_required(login_url='customerlogin')
def payment_success_view(request):
    # Here we will place order | after successful payment
    # we will fetch customer  mobile, address, Email
    # we will fetch product id from cookies then respective details from db
    # then we will create order objects and store in db
    # after that we will delete cookies because after order placed...cart should be empty
    customer=models.customer.objects.get(user_id=request.user.id)
    products=None
    email=models.customer.email
    mobile=None
    region=None
    barangay=None
    zipcode=None
    street=None
    detailed_address=None
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_id_in_cart=product_ids.split('|')
            products=models.Product.objects.all().filter(id__in = product_id_in_cart)
            # Here we get products list that will be ordered by one customer at a time
    # these things can be change so accessing at the time of order...
    if 'email' in request.COOKIES:
        email=request.COOKIES['email']
    if 'mobile' in request.COOKIES:
        mobile=request.COOKIES['mobile']
    if 'region' in request.COOKIES:
        region=request.COOKIES['region']
    if 'barangay' in request.COOKIES:
        barangay=request.COOKIES['barangay']
    if 'zipcode' in request.COOKIES:
        zipcode=request.COOKIES['zipcode']    
    if 'street' in request.COOKIES:
        street=request.COOKIES['street']
    if 'detailed_address' in request.COOKIES:
        detailed_address=request.COOKIES['detailed_address']
    # here we are placing number of orders as much there is a products
    # suppose if we have 5 items in cart and we place order....so 5 rows will be created in orders table
    # there will be lot of redundant data in orders table...but its become more complicated if we normalize it
    for product in products:
        models.Orders.objects.get_or_create(customer=customer,product=product,status='Pending',email=email,mobile=mobile,region=region,barangay=barangay,zipcode=zipcode,street=street,detailed_address=detailed_address)

    # after order placed cookies should be deleted
    response = render(request,'payment-success.html')
    response.delete_cookie('product_ids')
    response.delete_cookie('email')
    response.delete_cookie('mobile')
    response.delete_cookie('region')
    response.delete_cookie('barangay')
    response.delete_cookie('zipcode')
    response.delete_cookie('street')
    response.delete_cookie('detailed_address')
    return response

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_order_view(request):
    #productID = request.COOKIES['product_ids']
    #product=models.Product.objects.get(id=productID)
    vat = 0.12
    #with_vat=product.price+(product.price*vat)
    customer=models.customer.objects.get(user_id=request.user.id)
    orders=models.Orders.objects.all().filter(customer_id = customer)
    ordered_products=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_products.append(ordered_product)
        
    return render(request,'my-order.html',{'data':zip(ordered_products,orders),'customer':customer})
 

# @login_required(login_url='customerlogin')
# @user_passes_test(is_customer)
# def my_order_view2(request):

#     products=models.Product.objects.all()
#     if 'product_ids' in request.COOKIES:
#         product_ids = request.COOKIES['product_ids']
#         counter=product_ids.split('|')
#         product_count_in_cart=len(set(counter))
#     else:
#         product_count_in_cart=0
#     return render(request,'ecom/my_order.html',{'products':products,'product_count_in_cart':product_count_in_cart})    



#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def download_invoice_view(request,orderID,productID):
    order=models.Orders.objects.get(id=orderID)
    product=models.Product.objects.get(id=productID)
    customer=models.customer.objects.get(user_id=request.user.id)
    vat = 0.12
    with_vat=product.price+(product.price*vat)
    total_price = 0
    f_region=customer.region_text
    three = ["National Capital Region (NCR)","Region I (Ilocos Region)","Region II (Cagayan Valley)","Region III (Central Luzon)","Region IV-A (CALABARZON)","Region V (Bicol Region)"]
    four = ["Region VI (Western Visayas)","Region VII (Central Visayas)","Region VIII (Eastern Visayas)"]
    five = ["Region IX (Zamboanga Peninzula)","Region X (Northern Mindanao)","Region XI (Davao Region)","Region XII (SOCCSKSARGEN)","Region XIII (Caraga)","Cordillera Administrative Region (CAR)","Autonomous Region in Muslim Mindanao (ARMM)"]
    print(f_region)
    sf_three = 300
    sf_four = 400
    sf_five = 500
    shipping_fee = 0
    total_price = 0
    for i in three:
        if i == f_region:
            total_price = with_vat+sf_three
            shipping_fee = sf_three
            print("three",total_price)
    for i in four:
        if i == f_region:
            total_price = with_vat+sf_four
            shipping_fee = sf_four
            print("four", total_price)
    for i in five:
        if i == f_region:
            total_price = with_vat+sf_five
            shipping_fee = sf_five
            print("five", total_price)
            
    mydict={
        'orderDate':order.order_date,
        'customerUsername':request.user,
        'customerEmail':customer.email,
        'customerMobile':customer.mobile,
        'region':customer.region_text,
        'barangay':customer.barangay_text,
        'zipcode':customer.zipcode,
        'street':customer.street,
        'detailed_address':customer.detailed_address,
        'orderStatus':order.status,

        'productName':product.name,
        'productImage':product.product_img,
        'productPrice':product.price,
        'productDescription':product.description,
        'customerFname':customer.user.first_name,
        'customerLname':customer.user.last_name,
        'with_vat':with_vat,
        'total_price': total_price,
        'shipping_fee':shipping_fee,
        'f_region':f_region
    }
    
    
    return render_to_pdf('download-invoice.html',mydict)


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_profile_view(request):
    customer=models.customer.objects.get(user_id=request.user.id)
    return render(request,'my-profile.html',{'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def edit_profile_view(request):
    customer=models.customer.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.customerUserForm(instance=user)
    customerForm=forms.customerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.customerUserForm(request.POST,instance=user)
        customerForm=forms.customerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
        return HttpResponseRedirect('my-profile')
    return render(request,'edit-profile.html',context=mydict)


#========================================================ADMIN GRAPHS========================================================
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views import generic
from fchub.models import Orders,Product,customer
from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse , response
import pandas as pd
from .forms import ProductForm, OrderForm
from django.db.models import Count

def orderView(request):
    pending = Orders.objects.filter(status='Pending').count()
    pending_no = int(pending)
    print('Total Pending Orders',pending_no)
    
   #order confirmed
    oc = Orders.objects.filter(status='Order Confirmed').count() 
    oc_no = int(oc)
    print('Total Order Confirmed',oc_no)
    
    #out for delivery
    ofd = Orders.objects.filter(status='Out for Delivery').count()
    ofd_no = int(ofd)
    print('Total Out For Delivery',ofd_no)
    
    #Delivered
    delivered = Orders.objects.filter(status='Delivered').count()
    del_no = int(delivered)
    print('Total Delivered',del_no)
    
    status_list = ['Pending','Order Confirmed','Out for Delivery', 'Delivered']
    number_list = [pending_no,oc_no,ofd_no,del_no]
    context = {'status_list':status_list,'number_list':number_list}
    return render(request,'admin-graphs.html',context)
    
def orderView2(request):   
    item = Orders.objects.all().values()
    df = pd.DataFrame(item)
    df1 = df.name.tolist()
    df = df['status'].tolist()
    mydict = {
        'df':df,
        'df1':df1
    }
    return render(request,'admin-graphs.html',context=mydict)

def showProducts(request):
    products=models.Product.objects.all()
    return render(request,'admin-graphs-products.html',{'Products':products})

def showStock(request):
    products=models.Product.objects.all()
    return render(request,'admin-graphs-stock.html',{'Products':products})

def showOrders(request):
    orders=models.Orders.objects.all()
    repeated_names = Orders.objects.values('status').annotate(Count('id')).order_by().filter(id__count__gt=0)   # <--- gt 0 will get all the objects having occurred in DB i.e is greater than 0
    context = {
        'orders': orders, 'repeated_names': repeated_names 
    }
    return render(request,'admin-graphs-Orderlist.html',context)
    

# admin view the product
@login_required(login_url='adminlogin')
def admin_analytics_view(request):
    analytics=models.analytics.objects.all()
    return render(request,'admin-analytics.html',{'analytics':analytics})

# admin add product by clicking on floating button
@login_required(login_url='adminlogin')
def admin_add_info_analytics_view(request):
    AnalyticsForm=forms.AnalyticsForm()
    if request.method=='POST':
        AnalyticsForm=forms.AnalyticsForm(request.POST, request.FILES)
        if AnalyticsForm.is_valid():
            AnalyticsForm.save()
        return HttpResponseRedirect('admin-analytics')
    return render(request,'admin-add-info-analytics.html',{'AnalyticsForm':AnalyticsForm})

@login_required(login_url='adminlogin')
def update_analytics_view(request,pk):
    analytics=models.analytics.objects.get(id=pk)
    AnalyticsForm=forms.AnalyticsForm(instance=analytics)
    if request.method=='POST':
        AnalyticsForm=forms.AnalyticsForm(request.POST,request.FILES,instance=analytics)
        if AnalyticsForm.is_valid():
            AnalyticsForm.save()
            return redirect('admin-analytics')
    return render(request,'admin-update-info-analytics.html',{'AnalyticsForm':AnalyticsForm})

@login_required(login_url='adminlogin')
def delete_analytics_view(request,pk):
    analytics=models.analytics.objects.get(id=pk)
    analytics.delete()
    return redirect('admin-analytics')



class adminGraphs(TemplateView):
    template_name = 'admin-graphs.html'

class adminGraphsProducts(TemplateView):
    template_name = 'admin-graphs-products.html'

class adminGraphsReference(TemplateView):
    template_name = 'admin-graphs-reference.html'

class adminGraphsOrderlist(TemplateView):
    template_name = 'admin-graphs-orderlist.html'
    
class adminGraphsAnalytics(TemplateView):
    template_name = 'admin-graphs-analytics.html'

class adminGraphsStock(TemplateView):
    template_name = 'admin-graphs-stock.html'
    
class adminGraphsOrder(TemplateView):
    template_name = 'admin-graphs-totalorder.html'    



