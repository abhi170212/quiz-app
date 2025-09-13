from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    total_upvotes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize image if it's too large
        if self.profile_picture and hasattr(self.profile_picture, 'path'):
            try:
                img = Image.open(self.profile_picture.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.profile_picture.path)
            except (IOError, ValueError):
                # Handle cases where the image file doesn't exist or is invalid
                pass
    
    def get_quiz_stats(self):
        from quizzes.models import QuizAttempt
        attempts = QuizAttempt.objects.filter(user=self.user)
        if attempts.exists():
            total_attempts = attempts.count()
            avg_score = attempts.aggregate(avg_score=models.Avg('score'))['avg_score']
            best_score = attempts.aggregate(max_score=models.Max('score'))['max_score']
            return {
                'total_attempts': total_attempts,
                'average_score': round(avg_score, 2) if avg_score else 0,
                'best_score': best_score or 0
            }
        return {
            'total_attempts': 0,
            'average_score': 0,
            'best_score': 0
        }
