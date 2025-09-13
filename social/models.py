from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Upvote(models.Model):
    upvoter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_upvotes')
    upvoted_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_upvotes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['upvoter', 'upvoted_user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.upvoter.username} upvoted {self.upvoted_user.username}"
    
    def save(self, *args, **kwargs):
        # Prevent self-upvoting
        if self.upvoter == self.upvoted_user:
            raise ValueError("Users cannot upvote themselves")
        super().save(*args, **kwargs)
        
        # Update the upvoted user's profile total_upvotes
        from profiles.models import UserProfile
        profile, created = UserProfile.objects.get_or_create(user=self.upvoted_user)
        profile.total_upvotes = self.upvoted_user.received_upvotes.count()
        profile.save()
    
    def delete(self, *args, **kwargs):
        user = self.upvoted_user
        super().delete(*args, **kwargs)
        
        # Update the upvoted user's profile total_upvotes after deletion
        from profiles.models import UserProfile
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.total_upvotes = user.received_upvotes.count()
        profile.save()

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_comments')
    profile_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_comments')
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.commenter.username} on {self.profile_owner.username}'s profile"
    
    def save(self, *args, **kwargs):
        # Mark as edited if content is being changed (not on creation)
        if self.pk and self.content != Comment.objects.get(pk=self.pk).content:
            self.is_edited = True
        super().save(*args, **kwargs)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['follower', 'following']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
    
    def save(self, *args, **kwargs):
        # Prevent self-following
        if self.follower == self.following:
            raise ValueError("Users cannot follow themselves")
        super().save(*args, **kwargs)
