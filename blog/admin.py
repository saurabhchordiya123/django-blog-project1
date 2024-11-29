# blog/admin.py
from django.contrib import admin
from .models import BlogPost

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','image','created_at')  # Columns to show in the list view

admin.site.register(BlogPost, BlogPostAdmin)


