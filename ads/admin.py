from django.contrib import admin
from .models import Category, Listing, Message, Favorite

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ["title", "seller", "category", "price", "condition", "is_sold", "is_active", "created_at"]
    list_filter = ["is_sold", "is_active", "condition", "category"]
    search_fields = ["title", "description"]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["sender", "recipient", "listing", "is_read", "created_at"]

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ["user", "listing", "created_at"]
