from django.contrib import admin

from .models import User, Tweet

# Register your models here.
admin.site.register(Tweet)
admin.site.register(User)

