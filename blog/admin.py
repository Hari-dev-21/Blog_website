from django.contrib import admin
from .models import Post, Category,AboutUs, PostComments
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('titles', 'contents')
    search_fields = ('titles', 'contents')
    list_filter  = ('category', 'created_at')

admin.site.register(Post, PostAdmin)
admin.site.register(Category)    
admin.site.register(AboutUs)    
admin.site.register(PostComments)    
