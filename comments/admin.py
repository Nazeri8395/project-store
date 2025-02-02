from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'commenting_user', 'approring_user', 'comment_text', 'is_active',]
    list_editable = ['is_active',]
    
    def save_model(self, request, obj, form, change):
        if obj.is_active and obj.approring_user is None: 
            obj.approring_user = request.user
        super().save_model(request, obj, form, change)