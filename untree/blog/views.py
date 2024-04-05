from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Teammate, Post, Contact
from store.models import Product
from .forms import ContactForm, SubscriptionForm


def about_us_view(request):
    teammates = Teammate.objects.all()

    context = {
        'teammates': teammates,
        'hero_title': 'About Us'
    }
    return render(request, 'blog/about.html', context=context)


def services_view(request):
    products = Product.objects.all()[:3]
    context = {
        'products': products,
        'hero_title': 'Services'
    }
    return render(request, 'blog/services.html', context=context)


def blog_view(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'hero_title': 'Blog'
    }
    return render(request, 'blog/blog.html', context=context)


def contact_us_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            contact.save()
            messages.success(request, 'Message sent')
            return redirect('contact')
    else:
        form = ContactForm()
        context = {'form': form,
                   'hero_title': 'Contact Us'
                   }
        return render(request, 'blog/contact.html', context=context)


def save_sub_view(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            sub = form.save()
            sub.save()
            return redirect('index')


