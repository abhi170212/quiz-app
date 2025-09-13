from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.paginator import Paginator
from .models import UserProfile
from quizzes.models import QuizAttempt
from social.models import Comment, Upvote

User = get_user_model()

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Get quiz attempts with pagination
    quiz_attempts_list = QuizAttempt.objects.filter(user=user).select_related('quiz').order_by('-completed_at')
    attempts_paginator = Paginator(quiz_attempts_list, 10)  # Show 10 attempts per page
    attempts_page_number = request.GET.get('attempts_page')
    quiz_attempts = attempts_paginator.get_page(attempts_page_number)
    
    # Get comments with pagination
    comments_list = Comment.objects.filter(profile_owner=user).select_related('commenter').order_by('-created_at')
    comments_paginator = Paginator(comments_list, 5)  # Show 5 comments per page
    comments_page_number = request.GET.get('comments_page')
    comments = comments_paginator.get_page(comments_page_number)
    
    # Check if current user has upvoted this profile
    has_upvoted = False
    if request.user.is_authenticated:
        has_upvoted = Upvote.objects.filter(upvoter=request.user, upvoted_user=user).exists()
    
    context = {
        'profile_user': user,
        'profile': profile,
        'quiz_attempts': quiz_attempts,
        'comments': comments,
        'has_upvoted': has_upvoted,
        'quiz_stats': profile.get_quiz_stats()
    }
    return render(request, 'profiles/profile.html', context)

@login_required
def my_profile(request):
    return redirect('profiles:profile', username=request.user.username)

@login_required
def edit_profile(request, username):
    if request.user.username != username:
        messages.error(request, 'You can only edit your own profile.')
        return redirect('profiles:profile', username=username)
    
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Handle form submission - simplified for now
        bio = request.POST.get('bio', '')
        location = request.POST.get('location', '')
        website = request.POST.get('website', '')
        github_url = request.POST.get('github_url', '')
        linkedin_url = request.POST.get('linkedin_url', '')
        
        profile.bio = bio
        profile.location = location
        profile.website = website
        profile.github_url = github_url
        profile.linkedin_url = linkedin_url
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profiles:profile', username=username)
    
    context = {
        'profile': profile
    }
    return render(request, 'profiles/edit_profile.html', context)
