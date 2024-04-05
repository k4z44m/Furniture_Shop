from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from pyexpat import model

from django.urls import reverse

from .models import Category, Product, Review, Order, Order, ShippingAddress
from django.views.generic import ListView, DetailView
from random import randint
from .forms import LoginForm, RegistrationForm, ReviewForm, ShippingForm
from django.contrib.auth import login, logout
from .utils import CartForAuthenticatedUser
import stripe
from untree import settings


class IndexListView(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/index.html'
    extra_context = {
        'hero_title': 'Modern Interior Design Studio'
    }
    login_url = 'login_register'

    def get_queryset(self):
        return Product.objects.all()[:3]


class ShopView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/shop.html'
    extra_context = {
        'hero_title': 'Shop'
    }


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'store/detail.html'
    extra_context = {
        'hero_title': 'Detail'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        products = Product.objects.all()
        data = []
        for i in range(4):
            random_index = randint(0, len(products) - 1)
            product = products[random_index]
            if product not in data:
                data.append(product)
        context['products'] = data
        if self.request.user.is_authenticated:
            context['review_form'] = ReviewForm()
        reviews = Review.objects.filter(product=Product.objects.get(slug=self.kwargs['slug']))
        reviews = reviews.order_by('created_at')
        context['reviews'] = reviews[:3]
        return context


def login_register(request):
    context = {
        'login_form': LoginForm(),
        'register_form': RegistrationForm(),
        'hero_title': 'Login Register',
    }
    return render(request, 'store/login_register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            return redirect('login_register')


def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login_register')
        else:
            return redirect('login_register')


def user_logout(request):
    logout(request)
    return redirect('index')


def save_review(request, slug):
    if request.method == 'POST':
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = Product.objects.get(slug=slug)
            review.save()
            return redirect('product', slug)


def cart(request):
    """Страница корзины"""
    if request.user.is_authenticated:
        cart_info = CartForAuthenticatedUser(request).get_cart_info()
        return render(request, 'store/cart.html', cart_info)
    else:
        return redirect('login_register')


def to_cart(request, product_id, action):
    """Добавление товара в корзину"""
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request, product_id, action)
        return redirect('cart')
    else:
        return redirect('login_register')


def checkout(request):
    """Оформление заказа"""
    cart_info = CartForAuthenticatedUser(request).get_cart_info()
    cart_info['shipping_form'] = ShippingForm()
    return render(request, 'store/checkout.html', cart_info)


def create_checkout_session(request):
    """Функция проведения оплаты"""
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        user_cart = CartForAuthenticatedUser(request)
        cart_info = user_cart.get_cart_info()
        shipping_form = ShippingForm(data=request.POST)
        if shipping_form.is_valid():
            address = shipping_form.save(commit=False)
            address.user = request.user
            address.order = cart_info['order']
            address.save()

        total_price = cart_info['cart_total_price']
        total_quantity = cart_info['cart_total_quantity']

        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Товары с Furni'
                    },
                    'unit_amount': int(total_price * 100)
                },
                'quantity': total_quantity
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success')),
            cancel_url=request.build_absolute_uri(reverse('cart')),
        )
        return redirect(session.url, 303)


def success_payment(request):
    """Функция успешного оплаты"""
    user_cart = CartForAuthenticatedUser(request)
    user_cart.clear()
    return render(request, 'store/thankyou.html')

