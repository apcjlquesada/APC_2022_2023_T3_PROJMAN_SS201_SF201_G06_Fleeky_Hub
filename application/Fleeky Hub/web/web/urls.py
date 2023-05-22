"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from fchub import views
from django.contrib.auth.views import LoginView,LogoutView
from django.conf import settings #add this
from django.conf.urls.static import static #add this

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name='index'),
    path('products',views.products_view,name='products'),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='logout.html'),name='logout'),

    path('admin-graphs',views.adminGraphs.as_view(), name='admin-graphs'),
    path('admin-graphs',views.orderView, name='admin-graphs'),
    
    path('admin-graphs-products',views.showProducts, name='admin-graphs-products'),
    path('admin-graphs-stock',views.showStock, name='admin-graphs-stock'),
    path('admin-graphs-orderlist',views.showOrders, name='admin-graphs-orderlist'),
    
    path('admin-graphs-reference',views.adminGraphsReference.as_view(), name='admin-graphs-reference'),
   
    path('admin-graphs-analytics',views.adminGraphsAnalytics.as_view(), name='admin-graphs-analytics'),
    
    path('admin-graphs-totalorder',views.adminGraphsOrder.as_view(), name='admin-graphs-totalorder'),
    
    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('view-customer', views.view_customer_view,name='view-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),

    #products
    path('admin-products', views.admin_products_view,name='admin-products'),
    path('admin-add-products', views.admin_add_product_view,name='admin-add-products'),
    path('delete-product/<int:pk>', views.delete_product_view,name='delete-product'),
    path('update-product/<int:pk>', views.update_product_view,name='update-product'),

    #materials
    path('admin-materials', views.admin_materials_view,name='admin-materials'),
    path('admin-add-materials', views.admin_add_materials_view,name='admin-add-materials'),
    path('delete-materials/<int:pk>', views.delete_materials_view,name='delete-materials'),
    path('update-materials/<int:pk>', views.update_materials_view,name='update-materials'),
    
    path('admin-view-booking', views.admin_view_booking_view,name='admin-view-booking'),
    path('delete-order/<int:pk>', views.delete_order_view,name='delete-order'),
    path('update-order/<int:pk>', views.update_order_view,name='update-order'),

    #analytics
    path('admin-analytics', views.admin_analytics_view,name='admin-analytics'),
    path('admin-add-info-analytics', views.admin_add_info_analytics_view,name='admin-add-info-analytics'),
    path('delete-analytics/<int:pk>', views.delete_analytics_view,name='delete-analytics'),
    path('update-analytics/<int:pk>', views.update_analytics_view,name='update-analytics'),
    
    #customer
    path('customersignup', views.customer_signup_view,name='customersignup'),
    path('customerlogin', LoginView.as_view(template_name='customerlogin.html'),name='customerlogin'),
    path('customer-home', views.customer_home_view,name='customer-home'),
    path('customer-products', views.customer_products_view,name='customer-products'),
    path('my-order', views.my_order_view,name='my-order'),
    
    # path('my-order', views.my_order_view2,name='my-order'),
    path('my-profile', views.my_profile_view,name='my-profile'),
    path('edit-profile', views.edit_profile_view,name='edit-profile'),
    path('customer-products',views.customer_products_view,name='customer-products'),
    path('download-invoice/<int:orderID>/<int:productID>', views.download_invoice_view,name='download-invoice'),

    #cart
    path('add-to-cart/<int:pk>', views.add_to_cart_view,name='add-to-cart'),
    path('cart', views.cart_view,name='cart'),
    path('remove-from-cart/<int:pk>', views.remove_from_cart_view,name='remove-from-cart'),
    path('customer-address', views.customer_address_view,name='customer-address'),
    path('payment', views.payment,name='payment'),
    path('payment-success', views.payment_success_view,name='payment-success'),
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
