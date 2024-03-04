from django.contrib import admin
from network.models import User, Post

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff")

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user" ,"body", "timestamp")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)