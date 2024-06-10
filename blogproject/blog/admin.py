from django.contrib import admin
from .models import *

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "created")
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created", "updated")

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile)
# admin.site.register(UserManager)