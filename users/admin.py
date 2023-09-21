from django.contrib import admin
from .models import User,JobPost

# Register your models here.
admin.site.register(User)
admin.site.register(JobPost)