from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('product/<slug:slug>', ProductDetail.as_view(), name='product'),
    path('sign_in/', login_register, name='login_register'),
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('save_review/<slug:slug>/', save_review, name='save_review'),
    path('cart/', cart, name='cart'),
    path('to_cart/<int:product_id>/<str:action>/', to_cart, name='to_cart'),
    path('checkout/', checkout, name='checkout'),
    path('payment/', create_checkout_session, name='payment'),
    path('success/', success_payment, name='success'),
]

