from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from quizzes.models import Quiz, Question

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample quiz data'

    def handle(self, *args, **options):
        # Get the admin user
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stdout.write(self.style.ERROR('No admin user found. Please create a superuser first.'))
            return

        # Create Python Quiz
        python_quiz, created = Quiz.objects.get_or_create(
            title='Python Fundamentals',
            defaults={
                'description': 'Test your knowledge of Python programming fundamentals.',
                'language': 'python',
                'difficulty': 'beginner',
                'created_by': admin_user,
                'time_limit': 30
            }
        )

        if created:
            # Python questions
            python_questions = [
                {
                    'question_text': 'What is the output of print(type(5.5))?',
                    'option_a': '<class \'int\'>',
                    'option_b': '<class \'float\'>',
                    'option_c': '<class \'double\'>',
                    'option_d': '<class \'number\'>',
                    'correct_answer': 'B'
                },
                {
                    'question_text': 'Which of the following is used to define a function in Python?',
                    'option_a': 'function',
                    'option_b': 'def',
                    'option_c': 'define',
                    'option_d': 'func',
                    'correct_answer': 'B'
                },
                {
                    'question_text': 'What is the correct syntax to create a list in Python?',
                    'option_a': 'list = (1, 2, 3)',
                    'option_b': 'list = {1, 2, 3}',
                    'option_c': 'list = [1, 2, 3]',
                    'option_d': 'list = <1, 2, 3>',
                    'correct_answer': 'C'
                },
                {
                    'question_text': 'Which method is used to add an element to the end of a list?',
                    'option_a': 'add()',
                    'option_b': 'append()',
                    'option_c': 'insert()',
                    'option_d': 'extend()',
                    'correct_answer': 'B'
                },
                {
                    'question_text': 'What does the len() function return?',
                    'option_a': 'The last element of a sequence',
                    'option_b': 'The length of a sequence',
                    'option_c': 'The type of a sequence',
                    'option_d': 'The first element of a sequence',
                    'correct_answer': 'B'
                }
            ]

            for i, q_data in enumerate(python_questions):
                Question.objects.create(quiz=python_quiz, **q_data)

        # Create JavaScript Quiz
        js_quiz, created = Quiz.objects.get_or_create(
            title='JavaScript Basics',
            defaults={
                'description': 'Test your understanding of JavaScript fundamentals.',
                'language': 'javascript',
                'difficulty': 'beginner',
                'created_by': admin_user,
                'time_limit': 25
            }
        )

        if created:
            js_questions = [
                {
                    'question_text': 'Which of the following is the correct way to declare a variable in JavaScript?',
                    'option_a': 'var x = 5;',
                    'option_b': 'variable x = 5;',
                    'option_c': 'declare x = 5;',
                    'option_d': 'x := 5;',
                    'correct_answer': 'A'
                },
                {
                    'question_text': 'What is the output of console.log(typeof null)?',
                    'option_a': 'null',
                    'option_b': 'undefined',
                    'option_c': 'object',
                    'option_d': 'boolean',
                    'correct_answer': 'C'
                },
                {
                    'question_text': 'Which method is used to add an element to the end of an array?',
                    'option_a': 'push()',
                    'option_b': 'add()',
                    'option_c': 'append()',
                    'option_d': 'insert()',
                    'correct_answer': 'A'
                },
                {
                    'question_text': 'What is the correct syntax for a for loop in JavaScript?',
                    'option_a': 'for (i = 0; i <= 5)',
                    'option_b': 'for (i = 0; i <= 5; i++)',
                    'option_c': 'for (var i = 0; i <= 5; i++)',
                    'option_d': 'for i = 1 to 5',
                    'correct_answer': 'C'
                },
                {
                    'question_text': 'Which operator is used to assign a value to a variable?',
                    'option_a': '*',
                    'option_b': '=',
                    'option_c': '-',
                    'option_d': 'x',
                    'correct_answer': 'B'
                }
            ]

            for i, q_data in enumerate(js_questions):
                Question.objects.create(quiz=js_quiz, **q_data)

        # Create Java Quiz
        java_quiz, created = Quiz.objects.get_or_create(
            title='Java Programming Basics',
            defaults={
                'description': 'Test your knowledge of Java programming concepts.',
                'language': 'java',
                'difficulty': 'intermediate',
                'created_by': admin_user,
                'time_limit': 35
            }
        )

        if created:
            java_questions = [
                {
                    'question_text': 'Which of the following is the correct way to declare a main method in Java?',
                    'option_a': 'public static void main(String args[])',
                    'option_b': 'static public void main(String[] args)',
                    'option_c': 'public static void main(String[] args)',
                    'option_d': 'All of the above',
                    'correct_answer': 'D'
                },
                {
                    'question_text': 'What is the size of int data type in Java?',
                    'option_a': '2 bytes',
                    'option_b': '4 bytes',
                    'option_c': '8 bytes',
                    'option_d': 'Platform dependent',
                    'correct_answer': 'B'
                },
                {
                    'question_text': 'Which of the following is not a Java keyword?',
                    'option_a': 'static',
                    'option_b': 'Boolean',
                    'option_c': 'void',
                    'option_d': 'private',
                    'correct_answer': 'B'
                },
                {
                    'question_text': 'What is the default value of a boolean variable in Java?',
                    'option_a': 'true',
                    'option_b': 'false',
                    'option_c': '0',
                    'option_d': 'null',
                    'correct_answer': 'B'
                },
                {
                    'question_text': 'Which method is used to find the length of a string in Java?',
                    'option_a': 'length()',
                    'option_b': 'size()',
                    'option_c': 'getSize()',
                    'option_d': 'getLength()',
                    'correct_answer': 'A'
                }
            ]

            for i, q_data in enumerate(java_questions):
                Question.objects.create(quiz=java_quiz, **q_data)

        # Create C++ Quiz
        cpp_quiz, created = Quiz.objects.get_or_create(
            title='C++ Programming Fundamentals',
            defaults={
                'description': 'Test your understanding of C++ programming concepts and syntax.',
                'language': 'cpp',
                'difficulty': 'intermediate',
                'created_by': admin_user,
                'time_limit': 40
            }
        )

        if created:
            cpp_questions = [
                {
                    'question_text': 'Which of the following is used to define a class in C++?',
                    'option_a': 'class',
                    'option_b': 'Class',
                    'option_c': 'define class',
                    'option_d': 'struct',
                    'correct_answer': 'A'
                },
                {
                    'question_text': 'What is the correct syntax for a constructor in C++?',
                    'option_a': 'constructor ClassName()',
                    'option_b': 'ClassName()',
                    'option_c': 'void ClassName()',
                    'option_d': 'new ClassName()',
                    'correct_answer': 'B'
                },
                {
                    'question_text': 'Which operator is used for pointer dereferencing in C++?',
                    'option_a': '&',
                    'option_b': '*',
                    'option_c': '->',
                    'option_d': '.',
                    'correct_answer': 'B'
                },
                {
                    'question_text': 'What is the size of int data type in most modern systems?',
                    'option_a': '2 bytes',
                    'option_b': '4 bytes',
                    'option_c': '8 bytes',
                    'option_d': 'System dependent',
                    'correct_answer': 'B'
                },
                {
                    'question_text': 'Which header file is required for cout in C++?',
                    'option_a': '<stdio.h>',
                    'option_b': '<iostream>',
                    'option_c': '<conio.h>',
                    'option_d': '<stdlib.h>',
                    'correct_answer': 'B'
                }
            ]

            for i, q_data in enumerate(cpp_questions):
                Question.objects.create(quiz=cpp_quiz, **q_data)

        # Create PHP Quiz
        php_quiz, created = Quiz.objects.get_or_create(
            title='PHP Web Development Basics',
            defaults={
                'description': 'Test your knowledge of PHP programming for web development.',
                'language': 'php',
                'difficulty': 'beginner',
                'created_by': admin_user,
                'time_limit': 20
            }
        )

        if created:
            php_questions = [
                {
                    'question_text': 'What does PHP stand for?',
                    'option_a': 'Personal Home Page',
                    'option_b': 'PHP: Hypertext Preprocessor',
                    'option_c': 'Private Home Page',
                    'option_d': 'Professional Hypertext Protocol',
                    'correct_answer': 'B'
                },
                {
                    'question_text': 'Which symbol is used to declare a variable in PHP?',
                    'option_a': '%',
                    'option_b': '@',
                    'option_c': '$',
                    'option_d': '#',
                    'correct_answer': 'C'
                },
                {
                    'question_text': 'How do you create a comment in PHP?',
                    'option_a': '/* comment */',
                    'option_b': '// comment',
                    'option_c': '# comment',
                    'option_d': 'All of the above',
                    'correct_answer': 'D'
                },
                {
                    'question_text': 'Which function is used to include a file in PHP?',
                    'option_a': 'include()',
                    'option_b': 'require()',
                    'option_c': 'include_once()',
                    'option_d': 'All of the above',
                    'correct_answer': 'D'
                },
                {
                    'question_text': 'What is the correct way to end a PHP statement?',
                    'option_a': ';',
                    'option_b': '.',
                    'option_c': ':',
                    'option_d': '!',
                    'correct_answer': 'A'
                }
            ]

            for i, q_data in enumerate(php_questions):
                Question.objects.create(quiz=php_quiz, **q_data)

        # Create advanced Python quiz
        python_advanced_quiz, created = Quiz.objects.get_or_create(
            title='Advanced Python Programming',
            defaults={
                'description': 'Test your advanced Python knowledge including OOP, decorators, and more.',
                'language': 'python',
                'difficulty': 'advanced',
                'created_by': admin_user,
                'time_limit': 45
            }
        )

        if created:
            python_advanced_questions = [
                {
                    'question_text': 'What is the output of: list(map(lambda x: x**2, [1, 2, 3]))?',
                    'option_a': '[1, 4, 9]',
                    'option_b': '[2, 4, 6]',
                    'option_c': '[1, 2, 3]',
                    'option_d': 'Error',
                    'correct_answer': 'A',
                    'explanation': 'The map function applies lambda x: x**2 to each element, squaring them.'
                },
                {
                    'question_text': 'Which method is called when an object is created in Python?',
                    'option_a': '__init__',
                    'option_b': '__new__',
                    'option_c': '__create__',
                    'option_d': '__construct__',
                    'correct_answer': 'A',
                    'explanation': '__init__ is the initializer method called after object creation.'
                },
                {
                    'question_text': 'What does the @property decorator do?',
                    'option_a': 'Makes a method static',
                    'option_b': 'Creates a getter method',
                    'option_c': 'Makes a method private',
                    'option_d': 'Creates a class method',
                    'correct_answer': 'B',
                    'explanation': '@property creates a getter method that can be accessed like an attribute.'
                },
                {
                    'question_text': 'What is a generator in Python?',
                    'option_a': 'A function that returns multiple values',
                    'option_b': 'A function that uses yield',
                    'option_c': 'An iterator object',
                    'option_d': 'All of the above',
                    'correct_answer': 'D',
                    'explanation': 'Generators are functions that use yield to return an iterator object with multiple values.'
                },
                {
                    'question_text': 'What is the difference between is and == in Python?',
                    'option_a': 'No difference',
                    'option_b': 'is checks identity, == checks equality',
                    'option_c': 'is checks equality, == checks identity',
                    'option_d': 'is is faster than ==',
                    'correct_answer': 'B',
                    'explanation': 'is checks if two variables refer to the same object, == checks if the values are equal.'
                }
            ]

            for i, q_data in enumerate(python_advanced_questions):
                Question.objects.create(quiz=python_advanced_quiz, **q_data)

        self.stdout.write(
            self.style.SUCCESS('Successfully created comprehensive sample quiz data!')
        )