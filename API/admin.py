from django.contrib import admin
from .models import User , BlogModels, Comment, CategoryModels

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(BlogModels)
class BlogModelAdmin(admin.ModelAdmin):
    list_display = ['Blog_title','Blog_Category']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment']

@admin.register(CategoryModels)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['Category']