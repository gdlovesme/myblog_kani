from django.contrib import admin

# Register your models here.
from main.models import *


class PostImageInLine(admin.TabularInline):
    model = PostImage
    max_num = 10
    min_num = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInLine, ]

admin.site.register(Category)
