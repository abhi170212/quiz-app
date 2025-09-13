from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from profiles.models import UserProfile
from quizzes.models import Quiz, QuizAttempt, UserAnswer
from social.models import Comment, Upvote
import random
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Create test users and sample interactions'

    def handle(self, *args, **options):
        # Create test users
        test_users_data = [
            {
                'username': 'alex_dev',
                'email': 'alex@example.com',
                'first_name': 'Alex',
                'last_name': 'Developer',
                'bio': 'Full-stack developer passionate about Python and JavaScript.',
                'location': 'San Francisco, CA'
            },
            {
                'username': 'sarah_code',
                'email': 'sarah@example.com',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'bio': 'Frontend developer specializing in React and modern web technologies.',
                'location': 'New York, NY'
            },
            {
                'username': 'mike_python',
                'email': 'mike@example.com',
                'first_name': 'Mike',
                'last_name': 'Chen',
                'bio': 'Data scientist and Python enthusiast. Machine learning is my passion!',
                'location': 'Seattle, WA'
            },
            {
                'username': 'jenny_java',
                'email': 'jenny@example.com',
                'first_name': 'Jenny',
                'last_name': 'Williams',
                'bio': 'Backend developer with expertise in Java and Spring framework.',
                'location': 'Austin, TX'
            }
        ]

        created_users = []
        for user_data in test_users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name']
                }
            )
            
            if created:
                user.set_password('testpass123')
                user.save()
                
                # Create profile
                profile, _ = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'bio': user_data['bio'],
                        'location': user_data['location']
                    }
                )
                
                created_users.append(user)
                self.stdout.write(f'Created user: {user.username}')
        
        # Get all test users
        all_users = list(User.objects.filter(username__in=[u['username'] for u in test_users_data]))
        
        # Create quiz attempts
        quizzes = Quiz.objects.all()
        if quizzes.exists() and all_users:
            for user in all_users:
                # Each user takes 2-3 random quizzes
                num_quizzes = random.randint(2, min(3, quizzes.count()))
                user_quizzes = random.sample(list(quizzes), num_quizzes)
                
                for quiz in user_quizzes:
                    questions = quiz.questions.all()
                    if not questions.exists():
                        continue
                    
                    # Simulate quiz performance
                    correct_answers = random.randint(int(questions.count() * 0.4), questions.count())
                    score = round((correct_answers / questions.count()) * 100, 2)
                    
                    attempt = QuizAttempt.objects.create(
                        user=user,
                        quiz=quiz,
                        score=score,
                        total_questions=questions.count(),
                        correct_answers=correct_answers,
                        time_taken=timedelta(minutes=random.randint(10, quiz.time_limit))
                    )
                    
                    self.stdout.write(f'Created attempt: {user.username} -> {quiz.title} ({score}%)')
        
        # Create comments
        comments_text = [
            'Great job on your quiz results!',
            'Your programming skills are impressive.',
            'Keep up the excellent work!',
            'Thanks for the helpful coding tips.',
            'Looking forward to more quiz attempts!'
        ]
        
        if len(all_users) >= 2:
            for i in range(10):
                commenter = random.choice(all_users)
                profile_owner = random.choice(all_users)
                
                if commenter != profile_owner:
                    Comment.objects.get_or_create(
                        commenter=commenter,
                        profile_owner=profile_owner,
                        defaults={'content': random.choice(comments_text)}
                    )
        
        # Create upvotes
        if len(all_users) >= 2:
            for i in range(15):
                upvoter = random.choice(all_users)
                upvoted_user = random.choice(all_users)
                
                if upvoter != upvoted_user:
                    Upvote.objects.get_or_create(
                        upvoter=upvoter,
                        upvoted_user=upvoted_user
                    )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created test users and sample data!')
        )