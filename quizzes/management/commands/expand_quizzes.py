from django.core.management.base import BaseCommand
from quizzes.models import Quiz, Question

class Command(BaseCommand):
    help = 'Add more questions to existing quizzes to reach 30 questions each'

    def handle(self, *args, **options):
        # Get all quizzes
        quizzes = Quiz.objects.all()
        
        for quiz in quizzes:
            current_count = quiz.questions.count()
            needed = max(0, 30 - current_count)
            
            if needed > 0:
                self.stdout.write(f'Adding {needed} questions to {quiz.title}...')
                
                # Add questions based on the quiz language
                if quiz.language == 'python':
                    self.add_python_questions(quiz, needed)
                elif quiz.language == 'javascript':
                    self.add_javascript_questions(quiz, needed)
                elif quiz.language == 'java':
                    self.add_java_questions(quiz, needed)
                elif quiz.language == 'cpp':
                    self.add_cpp_questions(quiz, needed)
                elif quiz.language == 'php':
                    self.add_php_questions(quiz, needed)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully expanded all quizzes to 30 questions!')
        )

    def add_python_questions(self, quiz, count):
        questions = [
            {
                'question_text': 'What is the output of: print(2 ** 3 ** 2)?',
                'option_a': '64',
                'option_b': '512',
                'option_c': '256',
                'option_d': '128',
                'correct_answer': 'B',
                'explanation': 'Exponentiation is right-associative, so 3**2 = 9, then 2**9 = 512'
            },
            {
                'question_text': 'Which method is used to remove whitespace from both ends of a string?',
                'option_a': 'strip()',
                'option_b': 'trim()',
                'option_c': 'clean()',
                'option_d': 'remove()',
                'correct_answer': 'A'
            },
            {
                'question_text': 'What is the difference between append() and extend() methods?',
                'option_a': 'No difference',
                'option_b': 'append() adds single element, extend() adds multiple',
                'option_c': 'extend() is faster',
                'option_d': 'append() is for strings only',
                'correct_answer': 'B'
            },
            {
                'question_text': 'What is a Python decorator?',
                'option_a': 'A design pattern',
                'option_b': 'A function that modifies another function',
                'option_c': 'A class method',
                'option_d': 'A variable type',
                'correct_answer': 'B'
            },
            {
                'question_text': 'Which keyword is used for exception handling in Python?',
                'option_a': 'catch',
                'option_b': 'except',
                'option_c': 'handle',
                'option_d': 'error',
                'correct_answer': 'B'
            }
        ]
        
        for i, q_data in enumerate(questions[:count]):
            Question.objects.create(quiz=quiz, **q_data)

    def add_javascript_questions(self, quiz, count):
        questions = [
            {
                'question_text': 'What is the difference between == and === in JavaScript?',
                'option_a': 'No difference',
                'option_b': '== checks type, === checks value',
                'option_c': '== checks value, === checks type and value',
                'option_d': '=== is faster',
                'correct_answer': 'C'
            },
            {
                'question_text': 'Which method is used to join array elements into a string?',
                'option_a': 'join()',
                'option_b': 'concat()',
                'option_c': 'merge()',
                'option_d': 'combine()',
                'correct_answer': 'A'
            },
            {
                'question_text': 'What is a closure in JavaScript?',
                'option_a': 'A loop construct',
                'option_b': 'A function with access to outer scope',
                'option_c': 'A class method',
                'option_d': 'An error type',
                'correct_answer': 'B'
            },
            {
                'question_text': 'Which method is used to remove the last element from an array?',
                'option_a': 'removeLast()',
                'option_b': 'deleteLast()',
                'option_c': 'pop()',
                'option_d': 'splice()',
                'correct_answer': 'C'
            },
            {
                'question_text': 'What does the "this" keyword refer to in JavaScript?',
                'option_a': 'The current function',
                'option_b': 'The global object',
                'option_c': 'The calling object',
                'option_d': 'The parent object',
                'correct_answer': 'C'
            }
        ]
        
        for i, q_data in enumerate(questions[:count]):
            Question.objects.create(quiz=quiz, **q_data)

    def add_java_questions(self, quiz, count):
        questions = [
            {
                'question_text': 'What is inheritance in Java?',
                'option_a': 'Code reusability mechanism',
                'option_b': 'Error handling method',
                'option_c': 'Memory management',
                'option_d': 'Loop construct',
                'correct_answer': 'A'
            },
            {
                'question_text': 'Which access modifier makes a member accessible only within the same package?',
                'option_a': 'private',
                'option_b': 'protected',
                'option_c': 'public',
                'option_d': 'package-private (default)',
                'correct_answer': 'D'
            },
            {
                'question_text': 'What is polymorphism in Java?',
                'option_a': 'Multiple inheritance',
                'option_b': 'Method overloading and overriding',
                'option_c': 'Interface implementation',
                'option_d': 'Exception handling',
                'correct_answer': 'B'
            },
            {
                'question_text': 'Which collection class is synchronized in Java?',
                'option_a': 'ArrayList',
                'option_b': 'HashMap',
                'option_c': 'Vector',
                'option_d': 'LinkedList',
                'correct_answer': 'C'
            },
            {
                'question_text': 'What is the difference between abstract class and interface?',
                'option_a': 'No difference',
                'option_b': 'Abstract class can have concrete methods',
                'option_c': 'Interface is faster',
                'option_d': 'Abstract class is deprecated',
                'correct_answer': 'B'
            }
        ]
        
        for i, q_data in enumerate(questions[:count]):
            Question.objects.create(quiz=quiz, **q_data)

    def add_cpp_questions(self, quiz, count):
        questions = [
            {
                'question_text': 'What is the difference between struct and class in C++?',
                'option_a': 'No difference',
                'option_b': 'struct members are public by default',
                'option_c': 'class is faster',
                'option_d': 'struct cannot have methods',
                'correct_answer': 'B'
            },
            {
                'question_text': 'What is RAII in C++?',
                'option_a': 'Random Access Array Implementation',
                'option_b': 'Resource Acquisition Is Initialization',
                'option_c': 'Rapid Application Interface Integration',
                'option_d': 'Runtime Array Index Implementation',
                'correct_answer': 'B'
            },
            {
                'question_text': 'Which operator is used for dynamic memory allocation in C++?',
                'option_a': 'malloc',
                'option_b': 'alloc',
                'option_c': 'new',
                'option_d': 'create',
                'correct_answer': 'C'
            },
            {
                'question_text': 'What is function overloading in C++?',
                'option_a': 'Multiple functions with same name but different parameters',
                'option_b': 'Calling too many functions',
                'option_c': 'Using functions incorrectly',
                'option_d': 'Creating infinite loops',
                'correct_answer': 'A'
            },
            {
                'question_text': 'What is a virtual function in C++?',
                'option_a': 'A function that does not exist',
                'option_b': 'A function declared with virtual keyword',
                'option_c': 'A template function',
                'option_d': 'An inline function',
                'correct_answer': 'B'
            }
        ]
        
        for i, q_data in enumerate(questions[:count]):
            Question.objects.create(quiz=quiz, **q_data)

    def add_php_questions(self, quiz, count):
        questions = [
            {
                'question_text': 'What is the difference between include and require in PHP?',
                'option_a': 'No difference',
                'option_b': 'require stops execution on failure',
                'option_c': 'include is faster',
                'option_d': 'require is deprecated',
                'correct_answer': 'B'
            },
            {
                'question_text': 'Which superglobal variable contains form data in PHP?',
                'option_a': '$FORM',
                'option_b': '$INPUT',
                'option_c': '$_POST',
                'option_d': '$DATA',
                'correct_answer': 'C'
            },
            {
                'question_text': 'What is the concatenation operator in PHP?',
                'option_a': '+',
                'option_b': '.',
                'option_c': '&',
                'option_d': '|',
                'correct_answer': 'B'
            },
            {
                'question_text': 'Which function is used to connect to a MySQL database in PHP?',
                'option_a': 'mysql_connect()',
                'option_b': 'db_connect()',
                'option_c': 'mysqli_connect()',
                'option_d': 'database_connect()',
                'correct_answer': 'C'
            },
            {
                'question_text': 'What is the scope resolution operator in PHP?',
                'option_a': '->',
                'option_b': '::',
                'option_c': '=>',
                'option_d': '.',
                'correct_answer': 'B'
            }
        ]
        
        for i, q_data in enumerate(questions[:count]):
            Question.objects.create(quiz=quiz, **q_data)