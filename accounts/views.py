from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserSearchForm

User = get_user_model()

def register_view(request):
    if request.user.is_authenticated:
        return redirect('quizzes:home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('quizzes:home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('quizzes:home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully been logged out.')
    return redirect('quizzes:home')

def user_search(request):
    users = []
    query = ''
    
    if request.method == 'GET' and 'q' in request.GET:
        query = request.GET.get('q', '').strip()
        if query:
            users = User.objects.filter(
                Q(username__icontains=query) | 
                Q(first_name__icontains=query) | 
                Q(last_name__icontains=query)
            ).exclude(id=request.user.id if request.user.is_authenticated else None)[:10]
    
    # AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        users_data = []
        for user in users:
            users_data.append({
                'username': user.username,
                'full_name': f'{user.first_name} {user.last_name}' if user.first_name else user.username,
                'profile_url': f'/profiles/profile/{user.username}/'
            })
        return JsonResponse({'users': users_data})
    
    return render(request, 'accounts/user_search.html', {
        'users': users,
        'query': query
    })
