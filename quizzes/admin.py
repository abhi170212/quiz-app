from django.contrib import admin
from .models import Quiz, Question, QuizAttempt, UserAnswer

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ('question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'difficulty', 'created_by', 'is_active', 'created_at')
    list_filter = ('language', 'difficulty', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new quiz
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'question_text', 'correct_answer', 'created_at')
    list_filter = ('quiz__language', 'correct_answer', 'created_at')
    search_fields = ('question_text', 'quiz__title')
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Truncate long question text in admin
        if obj and len(obj.question_text) > 50:
            form.base_fields['question_text'].help_text = obj.question_text[:100] + '...'
        return form

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'correct_answers', 'total_questions', 'completed_at')
    list_filter = ('quiz__language', 'quiz', 'completed_at')
    search_fields = ('user__username', 'quiz__title')
    readonly_fields = ('user', 'quiz', 'score', 'correct_answers', 'total_questions', 'time_taken', 'completed_at')
    
    def has_add_permission(self, request):
        return False  # Prevent manual creation

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_answer', 'is_correct')
    list_filter = ('is_correct', 'selected_answer')
    search_fields = ('attempt__user__username', 'question__question_text')
    readonly_fields = ('attempt', 'question', 'selected_answer', 'is_correct')
    
    def has_add_permission(self, request):
        return False  # Prevent manual creation
