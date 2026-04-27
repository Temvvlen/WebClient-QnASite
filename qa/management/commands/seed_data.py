from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from qa.models import Question, Answer


class Command(BaseCommand):
    help = 'Seed database with sample users, questions, and answers'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Create 5 users
        users = []
        for i in range(1, 6):
            user, created = User.objects.get_or_create(username=f'user{i}')
            if created:
                user.set_password('test1234')
                user.save()
                self.stdout.write(f'  Created user{i}')
            else:
                self.stdout.write(f'  user{i} already exists')
            users.append(user)

        # Sample questions
        questions_data = [
            ("How do I use Django ORM?", "I'm new to Django and want to learn how to query the database using the ORM instead of raw SQL."),
            ("What is the difference between GET and POST?", "Can someone explain when to use GET vs POST in HTTP requests?"),
            ("How to use Bootstrap 5 cards?", "I want to display content in Bootstrap card components. How do I set them up properly?"),
            ("What is CSRF protection?", "Django requires {% csrf_token %} in forms. What is CSRF and why is it important?"),
            ("How does Django session management work?", "I want to understand how Django handles user sessions after login."),
            ("What is a ForeignKey in Django models?", "How do I create relationships between models using ForeignKey?"),
            ("How to use @login_required decorator?", "I want to restrict certain views to logged-in users only. How do I do this?"),
            ("What is the purpose of manage.py migrate?", "What does migrate do and when should I run it?"),
            ("How to pass data from views to templates?", "I want to send variables from my view function to the HTML template."),
            ("What is the difference between CharField and TextField?", "When should I use CharField vs TextField in my Django model?"),
        ]

        questions = []
        for i, (title, content) in enumerate(questions_data):
            author = users[i % len(users)]
            q, created = Question.objects.get_or_create(
                title=title,
                defaults={'content': content, 'author': author}
            )
            questions.append(q)
            if created:
                self.stdout.write(f'  Created question: {title[:40]}...')

        # Sample answers
        answers_data = [
            "Great question! You can use Model.objects.filter() to query, and Model.objects.all() to get everything.",
            "GET is for retrieving data (visible in URL), POST is for submitting data (hidden in request body). Use POST for forms.",
            "Wrap your content in <div class='card'><div class='card-body'>...</div></div> and add Bootstrap CDN to your HTML.",
            "CSRF (Cross-Site Request Forgery) prevents malicious sites from making requests on behalf of users. Always include the token!",
            "Django uses cookies to store a session ID, and stores session data server-side. login() function creates the session.",
            "ForeignKey creates a many-to-one relationship. Use on_delete=models.CASCADE to delete related objects automatically.",
            "Add @login_required above your view function. Unauthenticated users will be redirected to the login page.",
            "migrate applies database schema changes defined in migration files. Run it after makemigrations.",
            "Pass a dictionary as the third argument to render(): return render(request, 'template.html', {'key': value})",
            "Use CharField with max_length for short text (names, titles). Use TextField for long text (articles, descriptions).",
        ]

        for i, (question, answer_text) in enumerate(zip(questions, answers_data)):
            author = users[(i + 2) % len(users)]
            Answer.objects.get_or_create(
                question=question,
                author=author,
                defaults={'content': answer_text}
            )

        self.stdout.write(self.style.SUCCESS('✅ Seed data created successfully!'))
        self.stdout.write('   Login with: user1 / test1234')
