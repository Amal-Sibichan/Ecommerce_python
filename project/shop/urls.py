
from django.urls import path
from.import views

urlpatterns = [
    path('',views.index,name='index'),


    path('cart',views.cart,name='cart'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('cart/delete/<int:cart_item_id>/',views. delete_cart_item, name='delete_cart_item'),


    path('shop',views.grid,name='shop'),
    path('contact',views.contact,name='contact'),
    path('checkout',views.checkout,name='checkout'),
    path('proceed',views.proceed,name='proceed'),
    path('accept',views.accept_order,name='accept'),
    path('track_order/<int:order_id>/', views.track_order, name='track_order'),
    


    path('register',views.register,name='register'),
    path('userlogin',views.ulog,name='userlogin'),
    path('logout',views.logout_u,name='logout'),
    path('search/',views.search_view, name='search_view'),
    path('pay',views.pay,name='pay'),
    path('success' ,views.success , name='success'),
    path('update-user', views.update, name='update-user'),
    path('update-Address', views.updateAddress, name='update-Address'),



    
    path('sellerregister',views.s_register,name='sellerregister'),
    path('sellerlogin',views.slog,name='sellerlogin'),
    path('sellerhome',views.shome,name='sellerhome'),
    path('slogout',views.logout_s,name='slogout'),
    path('on',views.on,name='on'),



    path('add',views.add,name='add'),
    path('add_address',views.address,name='add_address'),
    path('uprofile',views.uprof,name='uprofile'),
    path('sprofile',views.sprof,name='sprofile'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),


]

    