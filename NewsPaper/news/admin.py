from django.contrib import admin
from .models import Post, Category, MyModel
from modeltranslation.admin import TranslationAdmin

# def nullfy_quantity(modeladmin, request, queryset):
#     queryset.update(quantity=0)
# nullfy_quantity.short_description = 'Удалить статью'

class PostsAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'post_type', 'date_in', 'rating')
    list_filter = ('author', 'post_type', 'date_in', 'rating')
    search_fields = ('author', 'post_type')
    # actions = [nullfy_quantity]


class CategoryAdmin(TranslationAdmin):
    model = Category




admin.site.register(MyModel)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostsAdmin)