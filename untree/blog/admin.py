from django.contrib import admin
from .models import Teammate, Contact, Post, Subscription


class TeammateAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'job']


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at']


class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email']


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email']


admin.site.register(Teammate, TeammateAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
