from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_upvotes', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'bio')
    readonly_fields = ('created_at', 'updated_at', 'total_upvotes')
    
    fields = ('user', 'bio', 'profile_picture', 'location', 'website', 'github_url', 'linkedin_url', 'total_upvotes', 'created_at', 'updated_at')
