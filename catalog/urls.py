from django.contrib import admin
from django.urls import path,include
from catalog import views

urlpatterns = [
    path('create/product', views.create_product , name='create_product'),
    path('signup/', views.user_signup, name="user_signup"),
    path("login/",views.user_login,name="user_login"),
    path("logout/",views.user_logout,name="user_logout"),
    path('product/<int:id>/', views.product_detail, name="product_detail"),
    path('list/product', views.list_product , name='list_product'),
    path('add/to/cart/<int:id>/',views.add_to_cart, name="add_to_cart"),
    path('my/cart/', views.cart_detail, name="cart_detail"),
    path('cart/delete/<int:id>/', views.cart_item_delete, name='cart_item_delete'),
    path('cart/edit/<int:id>/', views.cart_item_update, name='cart_item_update'),
    path('create/category', views.create_category , name='create_category'),
    path('list/category', views.list_category , name='list_category'),
    path('checkout/', views.order_checkout , name='order_checkout'),
    path('delivery/address/<int:id>/',views.order_delivery_address,name='order_delivery_address'),
    path('place/order/<int:id>/',views.place_order,name='place_order'),    path('payment/<int:id>/',views.make_payment,name='make_payment'),
    path('update/product<int:id>/', views.update_product , name='update_product'),
    path('delete/product/<int:id>/', views.delete_product, name='delete_product'),
    path("", views.home, name='home'),
]