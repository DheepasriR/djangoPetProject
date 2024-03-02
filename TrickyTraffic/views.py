# Create your views here.
from datetime import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import UserRegisterForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.utils import timezone
from django.shortcuts import redirect
from .models import Quiz, Question, Answer
from django.views import View
from django.shortcuts import render


# View for user registration
class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()  # Instantiate the UserRegisterForm
        return render(request, 'register.html', {'form': form})  # Render the registration form template

    def post(self, request):
        form = UserRegisterForm(request.POST)  # Instantiate the UserRegisterForm with form data
        if form.is_valid():  # Check if the form data is valid
            print(form.cleaned_data)  # Print the cleaned form data for reference
            user = form.save()  # Save the user instance
            print("Success message being generated")  # Print a success message
            messages.success(request, 'Your account has been successfully registered. You can now log in.')
            return redirect('login')  # Redirect the user to the login page
        else:
            print(form.errors)
            print("Form is not valid")  # Print an error message if the form is not valid
            messages.error(request, 'There was an error in the registration form. Please check your inputs.')
        return render(request, 'register.html', {'form': form})  # Re-render the registration form template


# View for the quiz
class QuizView(View):
    def get(self, request):
        questions = Question.objects.order_by('?')[:5]  # Retrieve 5 random questions
        return render(request, 'quiz.html', {'questions': questions})

    def post(self, request):
        user = request.user
        total_score = 0
        total_questions = 0

        quiz = Quiz(user=user, quiz_taken_datetime=timezone.now())  # Create a new quiz instance
        quiz.save()

        for question_id, selected_choice in request.POST.items():  # Process each submitted answer
            if question_id.startswith('question_'):
                total_questions += 1
                question_id = question_id.replace('question_', '')
                question = get_object_or_404(Question, pk=question_id)
                correct_choice = question.correct_choice

                if selected_choice == correct_choice:  # Check if the submitted answer is correct
                    total_score += 1

                answer = Answer(quiz=quiz, question=question,
                                selected_choice=selected_choice)  # Create and save the answer associated with the quiz
                answer.save()

        if total_questions > 0:  # Calculate score percentage
            score_percentage = (total_score / total_questions) * 100
        else:
            score_percentage = 0

        quiz.score = score_percentage  # Update quiz score and save
        quiz.save()

        return redirect('thank_you')  # Redirect to the thank you page


# View for the user's score
class ScoreView(View):
    def get(self, request):
        user = request.user  # Get the current user
        quizzes = Quiz.objects.filter(user=user)  # Get all quizzes for the current user

        total_quizzes = quizzes.count()  # Get the total number of quizzes taken
        if total_quizzes > 0:  # Check if quizzes have been taken
            total_score = sum(quiz.score for quiz in quizzes)  # Calculate the scores
            average_score = (total_score / total_quizzes)
            highest_score = max(quiz.score for quiz in quizzes)
            lowest_score = min(quiz.score for quiz in quizzes)
        else:
            total_score = 0  # Set default values
            average_score = 0
            highest_score = 0
            lowest_score = 0

        answers = Answer.objects.filter(quiz__in=quizzes)  # Get all answers for the quizzes

        context = {
            'total_score': total_score,
            'average_score': average_score,
            'highest_score': highest_score,
            'lowest_score': lowest_score,
            'quizzes': quizzes,
            'answers': answers,
        }
        return render(request, 'score.html', context)  # Render the score template with context


# View for custom login
class CustomLoginView(LoginView):
    template_name = 'login.html'  # Set the template name for the login view

    def form_valid(self, form):  # Override the form_valid method
        remember_me = form.cleaned_data.get('remember_me')  # Get the remember_me field value
        if not remember_me:  # Check if remember_me is not checked
            self.request.session.set_expiry(0)  # Set the session expiry to 0 (no remembering)
        return super().form_valid(form)  # Call the parent form_valid method

    def get_success_url(self):  # Override the get_success_url method
        return reverse_lazy('main-page')  # Return the URL of the main page


# View for the main page
class MainPageView(View):
    template_name = 'main_page.html'  # Set the template name for the main page

    def get(self, request):  # Override the get method
        return render(request, self.template_name)  # Render the main page template


# View for user logout
def logout_view(request):  # Define the logout view
    logout(request)  # Log the user out
    return redirect('main-page')  # Redirect the user to the main page


# View for the base template
def base_view(request):  # Define the base view
    return render(request, 'base.html')  # Render the base template


# View for reviewing quiz
class ReviewQuizView(View):
    template_name = 'review_quiz.html'  # Set the template name for the review quiz page

    def get(self, request, quiz_id):  # Override the get method
        quiz = get_object_or_404(Quiz, id=quiz_id)  # Get the quiz instance based on quiz_id
        answers = Answer.objects.filter(quiz=quiz)  # Get all answers for the quiz
        return render(request, self.template_name,
                      {'quiz': quiz, 'answers': answers})  # Render the review quiz template with context


def thank_you(request):
    return render(request, 'thank_you.html')
