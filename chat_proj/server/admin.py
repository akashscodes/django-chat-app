from django.contrib import admin

from .models import Server, Channel, Category


admin.site.register(Server)
admin.site.register(Channel)
admin.site.register(Category)
