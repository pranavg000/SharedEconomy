from django.urls import path, re_path
from . import views

app_name = 'core'

urlpatterns= [
    path('',views.home,name='home'),
    # path('buyer/', views.buyer, name="buyer"),
    re_path(r'^buyer/(?:(?P<pno>[0-9]+)/)?$', views.buyer, name="buyer"),
    path('traveller/', views.traveller, name="traveller"),
    path('allocate/', views.allocate, name="allocate"),
    path('load/', views.loadProducts, name="load"),
    path('cart/', views.cart, name="cart"),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('checkout/',views.checkout,name="checkout"),
    re_path(r'^buyprod/(?P<id>[0-9]+)/$', views.buyProd, name="buyProd"),
    re_path(r'^addtocart/$', views.addToCart, name="addToCart"),
    path('cartquantity/', views.cartquantity, name="cartquantity"),
    path('deletecart/', views.deleteCart, name="deletecart"),
    path('buyerdelete/', views.buyerdelete, name="buyerdelete"),
    path('travellerdelete/', views.travellerdelete, name="travellerdelete"),


]