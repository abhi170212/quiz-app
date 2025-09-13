from django.contrib import admin
from .models import Upvote, Comment, Follow

@admin.register(Upvote)
class UpvoteAdmin(admin.ModelAdmin):
    list_display = ('upvoter', 'upvoted_user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('upvoter__username', 'upvoted_user__username')
    readonly_fields = ('created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('commenter', 'profile_owner', 'content_preview', 'is_edited', 'created_at')
    list_filter = ('is_edited', 'created_at')
    search_fields = ('commenter__username', 'profile_owner__username', 'content')
    readonly_fields = ('created_at', 'updated_at', 'is_edited')
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('follower__username', 'following__username')
    readonly_fields = ('created_at',)
