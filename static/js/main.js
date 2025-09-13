// QuizHub JavaScript Functions

// CSRF Token handling
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Quiz Timer functionality
class QuizTimer {
    constructor(duration, onTick, onExpire) {
        this.duration = duration; // in seconds
        this.remaining = duration;
        this.onTick = onTick;
        this.onExpire = onExpire;
        this.interval = null;
        this.isRunning = false;
    }

    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.interval = setInterval(() => {
            this.remaining--;
            
            if (this.onTick) {
                this.onTick(this.remaining);
            }
            
            if (this.remaining <= 0) {
                this.stop();
                if (this.onExpire) {
                    this.onExpire();
                }
            }
        }, 1000);
    }

    stop() {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
            this.isRunning = false;
        }
    }

    getTimeElapsed() {
        return this.duration - this.remaining;
    }

    formatTime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        
        if (hours > 0) {
            return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }
}

// Quiz taking functionality
class QuizApp {
    constructor() {
        this.answers = {};
        this.currentQuestion = 1;
        this.totalQuestions = 0;
        this.timer = null;
        this.startTime = new Date();
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupTimer();
        this.updateProgress();
    }

    setupEventListeners() {
        // Option selection
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('option-btn')) {
                this.selectOption(e.target);
            }
        });

        // Navigation buttons
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const submitBtn = document.getElementById('submitBtn');

        if (prevBtn) {
            prevBtn.addEventListener('click', () => this.prevQuestion());
        }
        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.nextQuestion());
        }
        if (submitBtn) {
            submitBtn.addEventListener('click', () => this.submitQuiz());
        }
    }

    setupTimer() {
        const timerElement = document.getElementById('timer');
        const timeLimitElement = document.getElementById('timeLimit');
        
        if (timerElement && timeLimitElement) {
            const timeLimit = parseInt(timeLimitElement.value);
            
            this.timer = new QuizTimer(
                timeLimit,
                (remaining) => this.updateTimerDisplay(remaining),
                () => this.handleTimeExpired()
            );
            
            this.timer.start();
        }
    }

    updateTimerDisplay(remaining) {
        const timerElement = document.getElementById('timer');
        if (!timerElement) return;

        const timeText = this.timer.formatTime(remaining);
        timerElement.querySelector('.timer-text').textContent = timeText;

        // Add warning classes
        timerElement.classList.remove('warning', 'danger');
        
        if (remaining <= 300) { // 5 minutes
            timerElement.classList.add('warning');
        }
        if (remaining <= 60) { // 1 minute
            timerElement.classList.add('danger');
        }
    }

    handleTimeExpired() {
        alert('Time\'s up! Submitting your quiz automatically.');
        this.submitQuiz();
    }

    selectOption(optionBtn) {
        const questionId = optionBtn.dataset.questionId;
        const optionValue = optionBtn.dataset.option;
        
        // Remove selection from other options in this question
        const questionOptions = document.querySelectorAll(`[data-question-id="${questionId}"]`);
        questionOptions.forEach(btn => btn.classList.remove('selected'));
        
        // Select this option
        optionBtn.classList.add('selected');
        
        // Store the answer
        this.answers[questionId] = optionValue;
        
        // Update submit button state
        this.updateSubmitButton();
    }

    prevQuestion() {
        if (this.currentQuestion > 1) {
            this.currentQuestion--;
            this.showQuestion(this.currentQuestion);
            this.updateProgress();
        }
    }

    nextQuestion() {
        if (this.currentQuestion < this.totalQuestions) {
            this.currentQuestion++;
            this.showQuestion(this.currentQuestion);
            this.updateProgress();
        }
    }

    showQuestion(questionNumber) {
        // Hide all questions
        document.querySelectorAll('.question-card').forEach(card => {
            card.style.display = 'none';
        });
        
        // Show current question
        const currentQuestionCard = document.querySelector(`[data-question-number="${questionNumber}"]`);
        if (currentQuestionCard) {
            currentQuestionCard.style.display = 'block';
        }
        
        // Update navigation buttons
        this.updateNavigationButtons();
    }

    updateNavigationButtons() {
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        
        if (prevBtn) {
            prevBtn.disabled = this.currentQuestion === 1;
        }
        if (nextBtn) {
            nextBtn.disabled = this.currentQuestion === this.totalQuestions;
        }
    }

    updateProgress() {
        const progressBar = document.querySelector('.quiz-progress-bar');
        if (progressBar) {
            const progress = (this.currentQuestion / this.totalQuestions) * 100;
            progressBar.style.width = `${progress}%`;
        }
        
        const progressText = document.getElementById('progressText');
        if (progressText) {
            progressText.textContent = `Question ${this.currentQuestion} of ${this.totalQuestions}`;
        }
    }

    updateSubmitButton() {
        const submitBtn = document.getElementById('submitBtn');
        if (submitBtn) {
            const answeredCount = Object.keys(this.answers).length;
            submitBtn.textContent = `Submit Quiz (${answeredCount}/${this.totalQuestions} answered)`;
            submitBtn.disabled = answeredCount === 0;
        }
    }

    async submitQuiz() {
        if (Object.keys(this.answers).length === 0) {
            alert('Please answer at least one question before submitting.');
            return;
        }

        const confirmed = confirm(`Are you sure you want to submit? You have answered ${Object.keys(this.answers).length} out of ${this.totalQuestions} questions.`);
        if (!confirmed) return;

        // Stop timer
        if (this.timer) {
            this.timer.stop();
        }

        // Calculate time taken
        const timeTaken = Math.floor((new Date() - this.startTime) / 1000);

        // Prepare submission data
        const submissionData = {
            answers: this.answers,
            time_taken: timeTaken
        };

        // Show loading
        const submitBtn = document.getElementById('submitBtn');
        if (submitBtn) {
            submitBtn.innerHTML = '<span class="spinner"></span> Submitting...';
            submitBtn.disabled = true;
        }

        try {
            const response = await fetch(window.location.href.replace('/take/', '/submit/'), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify(submissionData)
            });

            const data = await response.json();

            if (data.success) {
                // Redirect to results page
                window.location.href = window.location.href.replace('/take/', `/result/${data.attempt_id}/`);
            } else {
                alert('Error submitting quiz: ' + data.message);
                if (submitBtn) {
                    submitBtn.innerHTML = 'Submit Quiz';
                    submitBtn.disabled = false;
                }
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Network error. Please try again.');
            if (submitBtn) {
                submitBtn.innerHTML = 'Submit Quiz';
                submitBtn.disabled = false;
            }
        }
    }
}

// Social interactions
async function toggleUpvote(username) {
    try {
        const response = await fetch(`/social/upvote/${username}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
            }
        });

        const data = await response.json();

        if (data.success) {
            const upvoteBtn = document.getElementById('upvoteBtn');
            const upvoteCount = document.getElementById('upvoteCount');

            if (upvoteBtn) {
                if (data.upvoted) {
                    upvoteBtn.classList.add('upvoted');
                    upvoteBtn.innerHTML = '<i class="fas fa-thumbs-up"></i> Upvoted';
                } else {
                    upvoteBtn.classList.remove('upvoted');
                    upvoteBtn.innerHTML = '<i class="far fa-thumbs-up"></i> Upvote';
                }
            }

            if (upvoteCount) {
                upvoteCount.textContent = data.total_upvotes;
            }
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Network error. Please try again.');
    }
}

async function addComment(username) {
    const commentInput = document.getElementById('commentInput');
    const content = commentInput.value.trim();

    if (!content) {
        alert('Please enter a comment.');
        return;
    }

    try {
        const formData = new FormData();
        formData.append('content', content);

        const response = await fetch(`/social/comment/${username}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            // Add comment to the page
            const commentsContainer = document.getElementById('commentsContainer');
            const commentHTML = `
                <div class="comment" id="comment-${data.comment.id}">
                    <div class="comment-header">
                        <strong>${data.comment.commenter_username}</strong>
                        <small class="comment-meta">${data.comment.created_at}</small>
                    </div>
                    <p>${data.comment.content}</p>
                </div>
            `;
            commentsContainer.insertAdjacentHTML('afterbegin', commentHTML);
            
            // Clear input
            commentInput.value = '';
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Network error. Please try again.');
    }
}

async function deleteComment(commentId) {
    if (!confirm('Are you sure you want to delete this comment?')) {
        return;
    }

    try {
        const response = await fetch(`/social/comment/delete/${commentId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const data = await response.json();

        if (data.success) {
            const commentElement = document.getElementById(`comment-${commentId}`);
            if (commentElement) {
                commentElement.remove();
            }
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Network error. Please try again.');
    }
}

// Initialize quiz app when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Initialize quiz app if we're on a quiz page
    if (document.querySelector('.quiz-container')) {
        window.quizApp = new QuizApp();
    }

    // Auto-resize textareas
    document.querySelectorAll('textarea').forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });

    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});

// Export functions for global use
window.toggleUpvote = toggleUpvote;
window.addComment = addComment;
window.deleteComment = deleteComment;