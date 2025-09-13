from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count, Avg, Max
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
import json
from .models import Quiz, Question, QuizAttempt, UserAnswer

User = get_user_model()

def home_view(request):
    quizzes = Quiz.objects.filter(is_active=True).annotate(
        total_questions=Count('questions'),
        total_attempts=Count('attempts')
    ).order_by('-created_at')
    
    # Filter by language if specified
    language = request.GET.get('language')
    if language:
        quizzes = quizzes.filter(language=language)
    
    context = {
        'quizzes': quizzes,
        'languages': Quiz.LANGUAGE_CHOICES,
        'selected_language': language
    }
    return render(request, 'quizzes/home.html', context)

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    user_attempts = []
    
    if request.user.is_authenticated:
        user_attempts = QuizAttempt.objects.filter(
            user=request.user, quiz=quiz
        ).order_by('-completed_at')[:5]
    
    context = {
        'quiz': quiz,
        'user_attempts': user_attempts,
        'total_questions': quiz.get_total_questions()
    }
    return render(request, 'quizzes/quiz_detail.html', context)

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    questions = quiz.questions.all().order_by('id')
    
    if questions.count() == 0:
        messages.error(request, 'This quiz has no questions yet.')
        return redirect('quizzes:quiz_detail', quiz_id=quiz.id)
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'total_questions': questions.count(),
        'time_limit_seconds': quiz.time_limit * 60
    }
    return render(request, 'quizzes/take_quiz.html', context)

@login_required
@require_POST
def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    questions = quiz.questions.all()
    
    if questions.count() == 0:
        return JsonResponse({'success': False, 'message': 'No questions in this quiz'})
    
    try:
        answers_data = json.loads(request.body)
        answers = answers_data.get('answers', {})
        time_taken_seconds = answers_data.get('time_taken', 0)
        
        correct_count = 0
        total_questions = questions.count()
        
        # Create quiz attempt
        time_taken = timedelta(seconds=time_taken_seconds)
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=0,  # Will update after calculating
            total_questions=total_questions,
            correct_answers=0,  # Will update after calculating
            time_taken=time_taken
        )
        
        # Process answers
        for question in questions:
            question_id = str(question.id)
            selected_answer = answers.get(question_id, '')
            
            is_correct = selected_answer == question.correct_answer
            if is_correct:
                correct_count += 1
            
            UserAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_answer=selected_answer,
                is_correct=is_correct
            )
        
        # Update attempt with final scores
        score_percentage = round((correct_count / total_questions) * 100, 2)
        attempt.correct_answers = correct_count
        attempt.score = score_percentage
        attempt.save()
        
        return JsonResponse({
            'success': True,
            'attempt_id': attempt.id,
            'score': score_percentage,
            'correct_answers': correct_count,
            'total_questions': total_questions
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid data format'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

def quiz_result(request, quiz_id, attempt_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, quiz=quiz)
    
    # Only allow viewing own results unless it's admin
    if request.user != attempt.user and not request.user.is_staff:
        messages.error(request, 'You can only view your own quiz results.')
        return redirect('quizzes:quiz_detail', quiz_id=quiz.id)
    
    user_answers = attempt.user_answers.select_related('question').order_by('question__id')
    
    context = {
        'quiz': quiz,
        'attempt': attempt,
        'user_answers': user_answers
    }
    return render(request, 'quizzes/quiz_result.html', context)

def leaderboard(request):
    # Get top scorers across all quizzes
    top_users = User.objects.annotate(
        total_attempts=Count('quiz_attempts'),
        avg_score=Avg('quiz_attempts__score'),
        best_score=Max('quiz_attempts__score')
    ).filter(total_attempts__gt=0).order_by('-avg_score', '-best_score')[:20]
    
    # Get recent high scores
    recent_attempts = QuizAttempt.objects.select_related('user', 'quiz').filter(
        score__gte=80
    ).order_by('-completed_at')[:10]
    
    context = {
        'top_users': top_users,
        'recent_attempts': recent_attempts
    }
    return render(request, 'quizzes/leaderboard.html', context)
