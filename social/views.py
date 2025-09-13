from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Upvote, Comment, Follow

User = get_user_model()

@login_required
@require_POST
def toggle_upvote(request, username):
    target_user = get_object_or_404(User, username=username)
    
    if request.user == target_user:
        return JsonResponse({'success': False, 'message': 'You cannot upvote yourself'})
    
    upvote, created = Upvote.objects.get_or_create(
        upvoter=request.user,
        upvoted_user=target_user
    )
    
    if not created:
        upvote.delete()
        upvoted = False
    else:
        upvoted = True
    
    total_upvotes = target_user.received_upvotes.count()
    
    return JsonResponse({
        'success': True,
        'upvoted': upvoted,
        'total_upvotes': total_upvotes
    })

@login_required
@require_POST
def add_comment(request, username):
    target_user = get_object_or_404(User, username=username)
    content = request.POST.get('content', '').strip()
    
    if not content:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Comment cannot be empty'})
        messages.error(request, 'Comment cannot be empty')
        return redirect('profiles:profile', username=username)
    
    comment = Comment.objects.create(
        commenter=request.user,
        profile_owner=target_user,
        content=content
    )
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'commenter_username': comment.commenter.username,
                'created_at': comment.created_at.strftime('%B %d, %Y at %I:%M %p')
            }
        })
    
    messages.success(request, 'Comment added successfully!')
    return redirect('profiles:profile', username=username)

@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Only profile owner can delete comments on their profile
    if request.user != comment.profile_owner:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Permission denied'})
        messages.error(request, 'You can only delete comments on your own profile.')
        return redirect('profiles:profile', username=comment.profile_owner.username)
    
    profile_owner_username = comment.profile_owner.username
    comment.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Comment deleted'})
    
    messages.success(request, 'Comment deleted successfully!')
    return redirect('profiles:profile', username=profile_owner_username)

@login_required
@require_POST
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)
    
    if request.user == target_user:
        return JsonResponse({'success': False, 'message': 'You cannot follow yourself'})
    
    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user
    )
    
    if not created:
        follow.delete()
        following = False
    else:
        following = True
    
    followers_count = target_user.followers.count()
    
    return JsonResponse({
        'success': True,
        'following': following,
        'followers_count': followers_count
    })
